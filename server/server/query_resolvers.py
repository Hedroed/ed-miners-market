from typing import Any, Dict, List, Optional
import os
from tartiflette import Resolver, TypeResolver

from .data import DataManager


manager = DataManager(os.environ.get('DB_PATH'), os.environ.get('MAPPING_PATH'))


@Resolver("Query.commodityMaxPrices")
async def resolve_query_max_prices(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning max commodity price over days.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: the list of all recipes
    :rtype: List[Dict[str, Any]]
    """
    return manager.get_commodity_max_prices(args["commodity_id"], args["days"])


@Resolver("Query.commodityPrices")
async def resolve_query_prices(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Optional[Dict[str, Any]]:
    """
    Resolver in charge of returning all max prices of each stations.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: a recipe
    :rtype: Optional[Dict[str, Any]]
    """
    return manager.get_commodity_prices(args["commodity_id"], args.get("timestamp",None), args["limit"])


@Resolver("Query.markets")
async def resolve_query_prices(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Optional[Dict[str, Any]]:
    """
    Resolver in charge of returning all markets.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: a recipe
    :rtype: Optional[Dict[str, Any]]
    """
    return manager.get_makets(args["limit"])

@Resolver("Query.market")
async def resolve_query_prices(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Optional[Dict[str, Any]]:
    """
    Resolver in charge of returning a market from this id.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: a recipe
    :rtype: Optional[Dict[str, Any]]
    """
    return manager.get_maket(args["id"])


@Resolver("Query.commodities")
async def resolve_query_prices(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Optional[Dict[str, Any]]:
    """
    Resolver in charge of returning all commodities.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: a recipe
    :rtype: Optional[Dict[str, Any]]
    """
    return manager.get_commodities(args["limit"])

@Resolver("Query.commodity")
async def resolve_query_prices(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Optional[Dict[str, Any]]:
    """
    Resolver in charge of returning a commodity from this id.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: a recipe
    :rtype: Optional[Dict[str, Any]]
    """
    return manager.get_commodity(args["id"])

