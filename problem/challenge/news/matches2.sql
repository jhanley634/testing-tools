
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

insert into players values(20, 2);
insert into players values(30, 1);
insert into players values(40, 3);
insert into players values(45, 1);
insert into players values(50, 2);
insert into players values(65, 1);

insert into matches values(1, 30, 45, 10, 12);
insert into matches values(2, 20, 50, 5, 5);
insert into matches values(13, 65, 45, 10, 10);
insert into matches values(5, 30, 65, 3, 15);
insert into matches values(42, 45, 65, 8, 4);

select m.*, p.group_id
from matches m
join players p on m.first_player = p.player_id
order by m.match_id
;

drop view  if exists  winning_score;
create view winning_score as
select
    p.group_id,
    coalesce(max(first_score, second_score), 0) as win_score
from players p
left join matches m on m.first_player = p.player_id
group by p.group_id
order by p.group_id
;
select * from winning_score;
