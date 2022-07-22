
drop table  if exists  players;
create table players (
    player_id  int primary key,
    group_id   int not null
);

drop table  if exists  matches;
create table matches (
    match_id       int primary key,
    first_player   int not null,
    second_player  int not null,
    first_score    int not null,
    second_score   int not null
);

delete from players;
delete from matches;

insert into players values (1, 11);
insert into players values (2, 11);
insert into players values (3, 13);
insert into players values (4, 13);

insert into matches values (101, 1, 2, 4, 5);
insert into matches values (102, 1, 2, 7, 6);
insert into matches values (103, 1, 2, 3, 4);
insert into matches values (104, 3, 4, 8, 9);

select m.*, p.group_id
from matches m
join players p on m.first_player = p.player_id
order by m.match_id
;
