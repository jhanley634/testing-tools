
-- cf https://www.sqlite.org/windowfunctions.html#built_in_window_functions

SELECT
    stamp,
    price,
    RANK() OVER (ORDER BY price) AS rnk
FROM price
WHERE price < 4
ORDER BY rnk
;
