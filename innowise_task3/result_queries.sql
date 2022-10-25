--1
SELECT c.name, COUNT(f.film_id) FROM public.film AS f
    INNER JOIN public.film_category AS fc on f.film_id = fc.film_id
    INNER JOIN public.category AS c ON fc.category_id = c.category_id
    GROUP BY c.category_id;

--2
SELECT a.first_name, a.last_name, COUNT(r.rental_id)
    FROM public.actor AS a
    INNER JOIN public.film_actor AS fa ON a.actor_id = fa.actor_id
    INNER JOIN public.film AS f ON fa.film_id = f.film_id
    INNER JOIN public.inventory AS inv ON f.film_id = inv.film_id
    INNER JOIN public.rental AS r ON inv.inventory_id = r.inventory_id
    GROUP BY a.first_name, a.last_name
    ORDER BY  COUNT(r.rental_id) DESC
    LIMIT 10;

--3
SELECT c.name  
    FROM public.category AS c
    INNER JOIN public.film_category AS fc ON c.category_id = fc.category_id
    INNER JOIN public.film AS f ON fc.film_id = f.film_id
    INNER JOIN public.inventory AS inv ON f.film_id = inv.film_id
    INNER JOIN public.rental AS r ON inv.inventory_id = r.inventory_id
    INNER JOIN public.payment AS p ON r.rental_id = p.rental_id
    GROUP BY c.name
    ORDER BY  sum(p.amount) DESC
    LIMIT 1 ;

--4
SELECT f.title  
    FROM film AS f
    LEFT JOIN inventory AS inv ON f.film_id = inv.film_id
    GROUP BY f.title
    HAVING count(inv.inventory_id) = 0 ;

--5
SELECT actor.first_name, actor.last_name, count(film.film_id)  
    FROM public.actor
    JOIN public.film_actor USING(actor_id)
    JOIN public.film USING(film_id)
    JOIN public.film_category on film.film_id = film_category.film_id
    JOIN public.category USING(category_id)
    WHERE category.name = 'Children'
    GROUP BY actor.first_name, actor.last_name
    ORDER BY count(film.film_id) DESC
    LIMIT 3 ;

--6
SELECT city.city, sum(customer.active), sum(abs(customer.active - 1))  
    FROM public.customer
    JOIN public.address USING(address_id)
    JOIN public.city USING(city_id)
    GROUP BY city.city
    ORDER BY sum(abs(customer.active - 1)) DESC ;


--7
WITH fin_table AS (SELECT category.name as category, city, rental_date, return_date
    FROM public.category
    JOIN public.film_category USING(category_id)
    JOIN public.film USING(film_id)
    JOIN public.inventory ON film.film_id = inventory.film_id
    JOIN public.rental USING(inventory_id)
    JOIN public.customer USING(customer_id)
    JOIN public.address USING(address_id)
    JOIN public.city USING(city_id))

(SELECT category, SUM(return_date - rental_date) FROM fin_table
    WHERE (city LIKE 'A%%' OR city LIKE 'a%%')
    GROUP BY category
    ORDER BY SUM(return_date - rental_date) DESC
    LIMIT 1)
UNION ALL
(SELECT category, SUM(return_date - rental_date) FROM fin_table
    WHERE city LIKE '%%-%%'
    GROUP BY category
    ORDER BY SUM(return_date - rental_date) DESC
    LIMIT 1 ) ;