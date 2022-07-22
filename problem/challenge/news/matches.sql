
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
    coalesce(min(mw.winner_id), p.player_id) as winner_id
from players p
left join match_winner mw on p.player_id = mw.winner_id
group by p.group_id
order by p.group_id
;
