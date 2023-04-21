create schema if not exists dds;

drop table if exists dds.h_user;

create table if not exists dds.h_user (
	h_user_pk  uuid primary key,
	user_id	varchar not null ,
	load_dt 	timestamp not null,
	load_src  varchar not null
);

drop table if exists dds.h_product;

create table if not exists dds.h_product  (
	h_product_pk  uuid primary key,
	product_id	varchar not null ,
	load_dt 	timestamp not null,
	load_src  varchar not null
);

drop table if exists dds.h_category;

create table if not exists dds.h_category  (
	h_category_pk  uuid primary key,
	category_name	varchar not null ,
	load_dt 	timestamp not null,
	load_src  varchar not null
);

drop table if exists dds.h_restaurant;

create table if not exists dds.h_restaurant  (
	h_restaurant_pk  uuid primary key,
	restaurant_id	varchar not null ,
	load_dt 	timestamp not null,
	load_src  varchar not null
);

drop table if exists dds.h_order;

create table if not exists dds.h_order  (
	h_order_pk  uuid primary key,
	order_id	int not null ,
	order_dt	timestamp not null,
	load_dt 	timestamp not null,
	load_src  varchar not null
);

drop table if exists dds.l_order_product;

create table if not exists dds.l_order_product  (
	hk_order_product_pk  uuid primary key,
	h_order_pk 	uuid references dds.h_order(h_order_pk) not null,
	h_product_pk 	uuid references dds.h_product(h_product_pk) not null,
	load_dt 	timestamp not null,
	load_src  varchar not null
);

drop table if exists dds.l_product_restaurant;

create table if not exists dds.l_product_restaurant  (
	hk_product_restaurant_pk  uuid primary key,
	h_product_pk 	uuid references dds.h_product(h_product_pk) not null,
	h_restaurant_pk 	uuid references dds.h_restaurant(h_restaurant_pk) not null,
	load_dt 	timestamp not null,
	load_src  varchar not null
);


drop table if exists dds.l_order_user;

create table if not exists dds.l_order_user   (
	hk_order_user_pk  uuid primary key,
	h_order_pk 	uuid references dds.h_order(h_order_pk) not null,
	h_user_pk 	uuid references dds.h_user(h_user_pk) not null,
	load_dt 	timestamp not null,
	load_src  varchar not null
);

drop table if exists dds.s_user_names;

create table if not exists dds.s_user_names (
	hk_user_names_pk  uuid not null,
	h_user_pk uuid references dds.h_user(h_user_pk) not null, 
	username varchar not null,
	userlogin varchar not null,
	load_dt 	timestamp not null,
	load_src  varchar not null
);

drop table if exists dds.s_product_names;

create table if not exists dds.s_product_names (
	hk_product_names_pk  uuid not null,
	h_product_pk uuid references dds.h_product(h_product_pk) not null, 
	name varchar not null,
	load_dt 	timestamp not null,
	load_src  varchar not null
);