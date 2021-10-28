
# Copyright 2021 John Hanley.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall
# the authors or copyright holders be liable for any claim, damages or
# other liability, whether in an action of contract, tort or otherwise,
# arising from, out of or in connection with the software or the use or
# other dealings in the software.

links = """
    <p>links</p>
    <ul>
      <li><a href="https://en.wikipedia.org/wiki/Kublai_Khan">Kublai_Khan</a>
      <li><a href="https://en.wikipedia.org/wiki/Stately_Pleasure_Dome">Coleridge</a>
      <li><a href="https://en.wikipedia.org/wiki/Ted_Nelson">Ted Nelson</a>
      <li><a href="https://en.wikipedia.org/wiki/Project_Xanadu#Original_17_rules">Xanadu</a>
      <li><a href="https://en.wikipedia.org/wiki/Tim_Berners-Lee">Sir Tim</a>
      <li><a href="https://upload.wikimedia.org/wikipedia/commons/d/d1/First_Web_Server.jpg">NeXT</a>
      <li><a href="https://w.wiki/4JMC">System 360</a>
      <li><a href="https://w.wiki/4JMD">3270</a>
      <li><a href="https://htmx.org/docs/">HTMx</a>
    </ul>
    <p>&nbsp;</p>
    <textarea rows="5" placeholder="today's date"></textarea>
    <p>&nbsp;</p>
"""

page_top = f"""
<!DOCTYPE html>
<html>
<head>
  <title>demo</title>
  <script src="https://unpkg.com/htmx.org@1.6.0"></script>
</head>
<body>
  <div>
    {links}
    <!-- have a button POST a click via AJAX -->
    <button hx-post="/clicked" hx-swap="outerHTML">Click Me</button>
  </div>
</body>
</html>
"""

page_bottom = """
    <p>&nbsp;</p>
    </ul>
      <li><a href="http://dc2-prod-data-3.internal.rexchange.com:8000/demo">demo</a>
    </ul>
"""
