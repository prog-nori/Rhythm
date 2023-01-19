create database rhythmdb;
use rhythmdb;

create table if not exists unchi (
    quantity int,
    time timestamp
);

create table if not exists queue (
    id int NOT NULL AUTOINCREMENT,  -- queueのid
    url varchar(64) NOT NULL,       -- 動画のURL
    server varchar(255) NOT NULL,   -- サーバ名
    author varchar(255),            -- 追加した人の名前（idではなく）
    status varchar(128) NOT NULL    -- 動画ステータス will / playing / played ??
);
