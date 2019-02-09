-- View: public.felino_dbinv

-- DROP VIEW public.felino_dbinv;

CREATE OR REPLACE VIEW public.felino_dbinv AS 
 SELECT min(t.barcode::text) AS id,
    t.article,
    t.list_prc,
    t.sale_price,
    count(*) AS count,
    json_agg(json_build_object('default_code', t.barcode, 'attribute_value_ids', t.ukuran) ORDER BY t.barcode) AS barcode_size,
    array_agg(t.index ORDER BY t.barcode) AS value_ids,
    array_agg(t.index ORDER BY t.barcode) AS idx,
    min(t.catagory::text) AS catagory,
    min(t.catid) AS min
   FROM ( SELECT felino_felino.article,
            felino_felino.list_prc,
            felino_felino.sale_price,
            felino_felino.barcode,
            felino_felino.ukuran,
            ( SELECT product_attribute_value.id
                   FROM product_attribute_value
                  WHERE product_attribute_value.name::text = felino_felino.ukuran::text AND product_attribute_value.attribute_id = 1
                 LIMIT 1) AS index,
            felino_felino.catagory,
            ( SELECT product_category.id
                   FROM product_category
                  WHERE product_category.name::text = felino_felino.catagory::text
                 LIMIT 1) AS catid
           FROM felino_felino
          ORDER BY felino_felino.barcode) t
  GROUP BY t.article, t.list_prc, t.sale_price;

ALTER TABLE public.felino_dbinv
  OWNER TO postgres;
