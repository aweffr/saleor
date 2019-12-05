import graphene
import graphene_django_optimizer as gql_optimizer

from ...stock import models
from ..core.fields import FilterInputConnectionField
from ..decorators import permission_required
from .filters import StockFilterInput
from .mutations import StockBulkDelete, StockCreate, StockDelete, StockUpdate
from .types import Stock


class StockQueries(graphene.ObjectType):
    stock = graphene.Field(
        Stock,
        description="Look up a stock by ID",
        id=graphene.ID(required=True, description="ID of an warehouse"),
    )
    stocks = FilterInputConnectionField(
        Stock,
        description="List of stocks.",
        filter=StockFilterInput(),
        query=graphene.String(),
    )

    @permission_required("stock.manage_stocks")
    def resolve_stock(self, info, **kwargs):
        stock_pk = kwargs.get("id")
        stock = graphene.Node.get_node_from_global_id(info, stock_pk, Stock)
        return stock

    @permission_required("stock.manage_stocks")
    def resolve_stocks(self, info, **data):
        qs = (
            models.Stock.objects.select_related("warehouse")
            .prefetch_related("product_variant__product")
            .all()
        )
        return gql_optimizer.query(qs, info)


class StockMutations(graphene.ObjectType):
    create_stock = StockCreate.Field()
    update_stock = StockUpdate.Field()
    delete_stock = StockDelete.Field()
    bulk_delete_stock = StockBulkDelete.Field()