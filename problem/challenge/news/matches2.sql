
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

drop view  if exists  match_winner;
create view match_winner as
select
    match_id,
    case
    when first_score = second_score then
        case
        when first_player < second_player
        then first_player
        else second_player
        end
    when first_score > second_score then first_player
    else second_player
    end as winner_id
from matches m
order by m.match_id
;
select
    p.group_id,
    min(mw.winner_id) as winner_id
from players p
join match_winner mw on p.player_id = mw.winner_id
group by p.group_id
order by p.group_id
;
