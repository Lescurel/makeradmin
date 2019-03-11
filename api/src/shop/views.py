from flask import g

from service.api_definition import WEBSHOP, WEBSHOP_EDIT, PUBLIC, GET, USER
from service.entity import Entity, OrmSingeRelation, OrmSingleSingleRelation
from shop import service
from shop.entities import product_image_entity, transaction_content_entity, transaction_entity, \
    transaction_action_entity, product_entity, category_entity
from shop.models import Action, ProductAction, TransactionContent
from shop.shop import pending_actions, member_history, receipt, get_product_data, list_product_data

service.entity_routes(
    path="/category",
    entity=category_entity,
    permission_list=WEBSHOP,
    permission_read=WEBSHOP,
    permission_create=WEBSHOP_EDIT,
    permission_update=WEBSHOP_EDIT,
    permission_delete=WEBSHOP_EDIT,
)


service.entity_routes(
    path="/product",
    entity=product_entity,
    permission_list=WEBSHOP,
    permission_read=WEBSHOP,
    permission_create=WEBSHOP_EDIT,
    permission_update=WEBSHOP_EDIT,
    permission_delete=WEBSHOP_EDIT,
)


service.related_entity_routes(
    path="/product/<int:related_entity_id>/images",
    entity=product_image_entity,
    relation=OrmSingeRelation('images', 'product_id'),
    permission_list=PUBLIC,
)


service.entity_routes(
    path="/action",
    entity=Entity(Action, default_sort_column=None),
    permission_list=WEBSHOP,
    permission_read=WEBSHOP,
    permission_create=WEBSHOP_EDIT,
    permission_update=WEBSHOP_EDIT,
)


service.entity_routes(
    path="/product_action",
    entity=Entity(ProductAction),
    permission_list=WEBSHOP,
    permission_read=WEBSHOP,
    permission_create=WEBSHOP_EDIT,
    permission_update=WEBSHOP_EDIT,
)


service.entity_routes(
    path="/transaction_content",
    entity=transaction_content_entity,
    permission_list=WEBSHOP,
    permission_read=WEBSHOP,
)


service.entity_routes(
    path="/transaction",
    entity=transaction_entity,
    permission_list=WEBSHOP,
    permission_read=WEBSHOP,
)

service.related_entity_routes(
    path="/transaction/<int:related_entity_id>/contents",
    entity=transaction_content_entity,
    relation=OrmSingeRelation('contents', 'transaction_id'),
    permission_list=WEBSHOP,
)


service.related_entity_routes(
    path="/transaction/<int:related_entity_id>/actions",
    entity=transaction_action_entity,
    relation=OrmSingleSingleRelation('actions', TransactionContent, 'transaction_id'),
    permission_list=WEBSHOP,
)


service.related_entity_routes(
    path="/member/<int:related_entity_id>/transactions",
    entity=transaction_entity,
    relation=OrmSingeRelation('member', 'member_id'),
    permission_list=WEBSHOP,
)


service.entity_routes(
    path="/product_image",
    entity=product_image_entity,
    permission_list=PUBLIC,
    permission_read=PUBLIC,
    permission_create=WEBSHOP_EDIT,
    permission_update=WEBSHOP_EDIT,
    permission_delete=WEBSHOP_EDIT,
)


@service.route("/member/current/pending_actions", method=GET, permission=USER)
def pending_actions_for_member():
    return pending_actions(g.user_id)


@service.route("/member/current/transactions", method=GET, permission=USER)
def transactions_for_member():
    return member_history(g.user_id)


@service.route("/member/current/receipt/<int:transaction_id>", method=GET, permission=USER)
def receipt_for_member(transaction_id):
    return receipt(g.user_id, transaction_id)


@service.route("/product_data", method=GET, permission=PUBLIC)
def list_product_data_view():
    return list_product_data()


@service.route("/product_data/<int:product_id>", method=GET, permission=PUBLIC)
def get_product_data_view(product_id):
    return get_product_data(product_id)

