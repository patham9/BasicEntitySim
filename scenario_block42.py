"""
 * The MIT License
 *
 * Copyright 2021 The OpenNARS authors.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 * """

from simulator import *
from enqueuer import *

entities = [
    entity(entityID=42, classID="block", spawnTime=0, terminationTime=50,
           spawnLocation=(0, 0), spawnAngle=0, spawnSpeed=100, color="red",
           behavior=[changeAngleAndSpeed(location=(WIDTH, 0), angle=-180, tolerance=100),
                     changeAngleAndSpeed(location=(0, 9), angle=0, tolerance=100)])
]

knowledge="""
*motorbabbling=0
*volume=0
<(<#entity --> [seen]> &/ <({SELF} * entitySeen) --> ^say>) =/> g>.
"""

goals="""
g! :|:
"""

enqueueSimulation(entities, t_start=0, t_end=50, firstPersonSpeed = 10, startSimNarsese = knowledge, endFrameNarsese=goals, endSimNarsese="")
