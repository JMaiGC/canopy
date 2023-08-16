from typing import List

from pinecone_text.hybrid import hybrid_convex_scale
from pinecone_text.dense.base_dense_ecoder import BaseDenseEncoder
from pinecone_text.sparse.base_sparse_encoder import BaseSparseEncoder

from context_engine.knoweldge_base.encoder.base import Encoder
from context_engine.knoweldge_base.models import KBQuery, KBEncodedDocChunk


# TODO: decide if we want to remove before release

class HybridEncoder(Encoder):
    """
    A hybrid encoder that combines dense embeddings and a sparse representation (e.g. keyword counts) using a
    linear combination
    """

    def __init__(self,
                 dense_encoder: BaseDenseEncoder,
                 sparse_encoder: BaseSparseEncoder,
                 default_alpha: float = 0.5,
                 **kwargs):
        """

        Args:
            dense_encoder: A DenseEncoder from pinecone_text that will be used to generate dense embeddings
            sparse_encoder: A SparseEncoder from pinecone_text that will be used to generate sparse
                            representations
            default_alpha: The default alpha value to use for scaling dense and sparse vectors. Defaults to 0.5.
                           Each query may include its own alpha value in the query_params dict, which will
                           override this value.

        Keyword Args:
            batch_size: The number of documents or queries to encode at once. Defaults to 1.
        """
        super().__init__(**kwargs)
        self.dense_encoder = dense_encoder
        self.sparse_encoder = sparse_encoder
        self.default_alpha = default_alpha

    def _encode_queries_batch(self, queries: List[KBQuery]):
        # NOTE: assumes that a DenseEncodingStep was run first
        values = self.dense_encoder.encode_query([q.text for q in queries])
        sparse_values = self.sparse_encoder.encode_query([q.text for q in queries])

        for query, val, sparse_val in zip(queries, values, sparse_values):
            alpha = query.query_params.get("alpha", self.default_alpha)
            query.values, query.sparse_values = hybrid_convex_scale(val, sparse_val, alpha)

    def _encode_documents_batch(self, documents: List[KBEncodedDocChunk]):
        pass

    async def _aencode_documents_batch(self, documents: List[KBEncodedDocChunk]):
        pass

    # Alters the queries in place
    async def _aencode_queries_batch(self, queries: List[KBQuery]):
        pass