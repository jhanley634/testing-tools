/*
Copyright 2020 John Hanley.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
The software is provided "AS IS", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall
the authors or copyright holders be liable for any claim, damages or
other liability, whether in an action of contract, tort or otherwise,
arising from, out of or in connection with the software or the use or
other dealings in the software.
*/

-- Produces version 4 guids for mysql, as its UUID() only offers version 1.
--
-- See https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)
-- We consider variant 1 only, ignoring the Microsoft proprietary variant 2.
-- Version 1 is predictable timestamp.
-- Version 4 is 122 random bits + 6 constant bits.
--
-- The nil guid comes out like this:
-- UUID('00000000-0000-4000-8000-000000000000')  # 8-4-4-4-12
-- The nybble '4' is constant.
-- The nybble '8' has hi bit set, next bit cleared, plus two wasted bits.
-- We deliberately choose to emit just 120 random bits, for simplicity.
-- The RAND() function returns about 53 bits of entropy in the mantissa,
-- so we call it five times to obtain 265 ( > 256 ) unguessable bits.
-- We wind up needing to do this thrice (15 calls) to gen a guid.
-- The standard spelling of a guid, with four '-' dashes, is 36 characters.
-- We emit 32 hex characters, sans dashes.


DROP TABLE  IF EXISTS  guid_test;
CREATE TABLE           guid_test (
  guid       CHARACTER(32)    PRIMARY KEY,
  updated    TIMESTAMP        NOT NULL  DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO guid_test (guid, updated) VALUES (
  concat(
    substr(sha2(concat(rand(), rand(), rand(), rand(), rand()), 256), 1, 12),
    '4',
    substr(sha2(concat(rand(), rand(), rand(), rand(), rand()), 256), 1,  3),
    '8',
    substr(sha2(concat(rand(), rand(), rand(), rand(), rand()), 256), 1, 15)
  ),
  now()
);
