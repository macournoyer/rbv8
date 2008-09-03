# Copyright 2008 Google Inc.  All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of Google Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import test
import os
from os.path import join, dirname, exists
import re


FLAGS_PATTERN = re.compile(r"//\s+Flags:(.*)")


class MjsunitTestCase(test.TestCase):

  def __init__(self, path, file, mode, context, config):
    super(MjsunitTestCase, self).__init__(context, path)
    self.file = file
    self.config = config
    self.mode = mode

  def GetLabel(self):
    return "%s %s" % (self.mode, self.GetName())

  def GetName(self):
    return self.path[-1]

  def GetCommand(self):
    result = [self.config.context.GetVm(self.mode)]
    source = open(self.file).read()
    flags_match = FLAGS_PATTERN.search(source)
    if flags_match:
      result += flags_match.group(1).strip().split()
    framework = join(dirname(self.config.root), 'mjsunit', 'mjsunit.js')
    result += [framework, self.file]
    return result


class MjsunitTestConfiguration(test.TestConfiguration):

  def __init__(self, context, root):
    super(MjsunitTestConfiguration, self).__init__(context, root)

  def Ls(self, path):
    def SelectTest(name):
      return name.endswith('.js') and name != 'mjsunit.js'
    return [f[:-3] for f in os.listdir(path) if SelectTest(f)]

  def ListTests(self, current_path, path, mode):
    mjsunit = [current_path + [t] for t in self.Ls(self.root)]
    regress = [current_path + ['regress', t] for t in self.Ls(join(self.root, 'regress'))]
    bugs = [current_path + ['bugs', t] for t in self.Ls(join(self.root, 'bugs'))]
    all_tests = mjsunit + regress + bugs
    result = []
    for test in all_tests:
      if self.Contains(path, test):
        file_path = join(self.root, reduce(join, test[1:], "") + ".js")
        result.append(MjsunitTestCase(test, file_path, mode, self.context, self))
    return result

  def GetBuildRequirements(self):
    return ['sample', 'sample=shell']

  def GetTestStatus(self, sections, defs):
    status_file = join(self.root, 'mjsunit.status')
    if exists(status_file):
      test.ReadConfigurationInto(status_file, sections, defs)



def GetConfiguration(context, root):
  return MjsunitTestConfiguration(context, root)