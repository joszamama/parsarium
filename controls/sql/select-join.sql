SELECT c.region, COUNT(*) AS order_count, SUM(o.total) AS revenue
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.id
WHERE o.status = 'paid' AND o.total >= 10
GROUP BY c.region
ORDER BY c.region;
