#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import os
import jinja2

from HairpinFinder import HairpinFinder


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))


class ResultsHandler(webapp2.RequestHandler):
    def post(self):
        target = self.request.get('target')
        others = self.request.get('others').splitlines()
        hairpin_finder = HairpinFinder(target, others)
        conserved = hairpin_finder.conserved

        self.response.write("<!DOCTYPE html>" +
                            '<html lang="en">' +
                            "<head>")
        self.style()
        self.response.write("</head>" +
                            "<body>")

        for conserved_hp in conserved:
            self.response.write('<div class="green-floral-box">TARGET:<br>')
            self.draw_hairpins([conserved_hp.target])

            self.response.write('<br>MATCHES:<br>')
            self.draw_hairpins(conserved_hp.matches)
            self.response.write("</div>")

    def style(self):
        self.response.write('<link type="text/css" rel="stylesheet" href="styles.css">')

    """
    'hairpins' should be a list of CountedHairpins objects.
    """
    def draw_hairpins(self, hairpins):
        if len(hairpins) == 0:
            return

        self.response.write('<table border="1"')

        # make header of table
        self.response.write("<tr>" +
                            "<th>Sequence</th>" +
                            "<th>Start</th>" +
                            "<th>End</th>" +
                            "<th>Stem Length (in base pairs)</th></th>" +
                            "<th>Loop Sequence</th>" +
                            "<th>Stability Score</th>" +
                            "</tr>")

        # add in hairpins
        for counted_hp in hairpins:
            hp = counted_hp.hp

            self.response.write("<tr>" +
                                "<td>" + hp.seq.name + "</th>" +
                                "<td>" + str(hp.stem[-1].pos1) + "</td>" +
                                "<td>" + str(hp.stem[-1].pos2) + "</td>" +
                                "<td>" + str(len(hp.stem)) + "</td>" +
                                "<td>" + hp.loop_seq + "</td>" +
                                "<td>")

            if counted_hp.score == 1:
                self.response.write("100.0%")
            else:
                self.response.write(str(counted_hp.score * 100)[:4] + "%")

            self.response.write("</td>" +
                                "</tr>")

        self.response.write("</table>")


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler)
], debug=True)
