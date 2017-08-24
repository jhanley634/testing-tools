
-- Copyright 2017 John Hanley.
--
-- Permission is hereby granted, free of charge, to any person obtaining a
-- copy of this software and associated documentation files (the "Software"),
-- to deal in the Software without restriction, including without limitation
-- the rights to use, copy, modify, merge, publish, distribute, sublicense,
-- and/or sell copies of the Software, and to permit persons to whom the
-- Software is furnished to do so, subject to the following conditions:
-- The above copyright notice and this permission notice shall be included in
-- all copies or substantial portions of the Software.
-- The software is provided "AS IS", without warranty of any kind, express or
-- implied, including but not limited to the warranties of merchantability,
-- fitness for a particular purpose and noninfringement. In no event shall
-- the authors or copyright holders be liable for any claim, damages or
-- other liability, whether in an action of contract, tort or otherwise,
-- arising from, out of or in connection with the software or the use or
-- other dealings in the software.

drop table  if exists  crumb_trip_point;
create table crumb_trip_point(
  file_no  integer        not null,
  stamp    timestamp      not null,
  lng      float          not null,
  lat      float          not null,
  bearing  decimal(6, 1)  not null,
  edge_id  integer        not null,
  rpm      integer        not null,
  speed    float          not null,
  primary key (file_no, stamp)
);
