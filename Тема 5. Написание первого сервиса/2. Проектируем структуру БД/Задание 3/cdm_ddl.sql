create schema if not exists cdm;

--drop table if exists cdm.user_product_counters;

create table if not exists cdm.user_product_counters (
	id	serial primary key,
	user_id	uuid not null,
	product_id	uuid not null,
	product_name	varchar not null,
	order_cnt int check (order_cnt >= 0) not null,
	constraint user_product_counters_unq unique(user_id,product_id)
);


create table if not exists cdm.user_category_counters (
	id	serial primary key,
	user_id	uuid not null,
	category_id	uuid not null,
	category_name	varchar not null,
	order_cnt int check (order_cnt >= 0) not null,
	constraint user_category_counters_unq unique(user_id,category_id)
);
