import ddt
from django.test import TestCase
from mock import Mock

from ecommerce.core.templatetags.core_extras import get_coupon_name
from ecommerce.extensions.basket.models import Basket, BasketAttribute, BasketAttributeType
from ecommerce.extensions.order.models import Order, OrderDiscount


@ddt.ddt
class CoreExtrasUtilsTests(TestCase):
    """Test class for utils implemented in templatetags."""

    def test_get_coupon_name_from_order(self):
        """This test checks that 'get_coupon_name' returns the coupon name from an
        Order object if the order has discounts."""
        coupon_name = 'coupon-name'
        voucher = Mock()
        voucher.name = coupon_name
        discount = Mock(voucher=voucher)
        order = Mock(spec=Order)
        order.basket_discounts.first.return_value = discount

        result = get_coupon_name(order)

        self.assertEqual(result, coupon_name)

    def test_get_coupon_name_from_order_without_voucher(self):
        """This test checks that 'get_coupon_name' returns an empty string
        if the order has no discounts, and therefore no voucher."""
        order = Mock(spec=Order)
        order.basket_discounts.first.return_value = None

        result = get_coupon_name(order)

        self.assertEqual(result, '')

    def test_get_coupon_name_from_basket(self):
        """This test checks that 'get_coupon_name' returns the coupon name from a
        Basket object if the basket has a voucher."""
        coupon_name = 'coupon-name'
        voucher = Mock()
        voucher.name = coupon_name
        basket = Mock(spec=Basket)
        basket.vouchers.first.return_value = voucher

        result = get_coupon_name(basket)

        self.assertEqual(result, coupon_name)

    def test_get_coupon_name_from_order_with_program_offer(self):
        """This test checks that 'get_coupon_name' returns an empty string
        if the order has a program offer discount, which means that the order
        has a discount but this type of discount has no voucher."""
        order = Mock(spec=Order)
        order_discount = Mock(spec=OrderDiscount)
        order_discount.voucher = None
        order.basket_discounts.first.return_value = order_discount

        result = get_coupon_name(order)

        self.assertEqual(result, '')

    def test_get_coupon_name_from_basket_without_voucher(self):
        """This test checks that 'get_coupon_name' returns an empty string
        if the basket has no voucher."""
        basket = Mock(spec=Basket)
        basket.vouchers.first.return_value = None

        result = get_coupon_name(basket)

        self.assertEqual(result, '')

    def test_get_coupon_name_from_orderdiscount(self):
        """This test checks that 'get_coupon_name' returns the coupon name from a
        OrderDiscount object if the object has a voucher."""
        coupon_name = 'coupon-name'
        order_discount = Mock(spec=OrderDiscount)
        order_discount.voucher.name = coupon_name

        result = get_coupon_name(order_discount)

        self.assertEqual(result, coupon_name)

    def test_get_coupon_name_from_orderdiscount_with_program_offer(self):
        """This test checks that 'get_coupon_name' returns an empty string
        if the order discount comes from a program offer, which means that the order
        has a discount but this type of discount has no voucher."""
        order_discount = Mock(spec=OrderDiscount)
        order_discount.voucher = None

        result = get_coupon_name(order_discount)

        self.assertEqual(result, '')

    @ddt.data(None, 'string', [], {'test-key': 'value'}, BasketAttributeType, BasketAttribute)
    def test_get_coupon_name_called_with_unexpected_argument(self, object_provided):
        """This test makes sure that 'get_coupon_name' returns an empty string when called with
        an argument which is none of these: 'OrderDiscount', 'Basket', or 'Order'."""
        result = get_coupon_name(object_provided)

        self.assertEqual(result, '')
