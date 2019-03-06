SELECT
    v.product_id AS productId,
    v.id AS skuId,
    p.purchase_prices AS purchasePrices,
    i.urls AS urls,
    inv.inventory_count AS inventoryCount
FROM `raw.variants` v
    LEFT JOIN `tmp.inventory_items` inv ON inv.variant_id = v.id
    LEFT JOIN `tmp.item_purchase_prices` p ON p.order_item_id = inv.order_item_id
    LEFT JOIN `tmp.variant_images` i ON i.variant_id = v.id
