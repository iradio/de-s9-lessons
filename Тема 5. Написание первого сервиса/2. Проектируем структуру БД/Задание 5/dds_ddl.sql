create schema if not exists dds;

drop table if exists dds.h_user;

create table if not exists dds.h_user (
	h_user_pk  uuid primary key,
	user_id	varchar not null ,
	load_dt 	timestamp not null,
	load_src  varchar not null
);
