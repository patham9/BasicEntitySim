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

from math import *
from copy import deepcopy
import random
random.seed(1337)

DefaultEntitySize = 100
#Entities in Clojure style dictionary types, no Python object boilerplate:
def entity(entityID, classID, spawnTime, terminationTime, spawnLocation, spawnAngle, spawnSpeed, color = "yellow", width = DefaultEntitySize, height = DefaultEntitySize, behavior=[]):
    return { "entityID": entityID, "classID": classID, "spawnTime": spawnTime, "terminationTime": terminationTime, "color": color, "width": width, "height" : height,
             "location": spawnLocation, "angle": radians(spawnAngle), "speed": spawnSpeed, "behavior": behavior, "history": []}

#The change of angle and speed at a certain location:
def changeAngleAndSpeed(location, angle = None, speed = None, tolerance=0.1):
    return { "location": location, "angle": radians(angle), "speed": speed, "tolerance": tolerance }

#Whether tracklet is alive
def alive(entity, t):
    return t >= entity["spawnTime"] and t < entity["terminationTime"]

#Whether two locations are similar
def similarLocation(loc1, loc2, tolerance):
    return sqrt((loc2[0]-loc1[0])**2 + (loc2[1]-loc1[1])**2) < tolerance

#Tracklet history entry
def trackletPoint(entity, W=50, H=50, P=100):
    return [int(entity["location"][0]), int(entity["location"][1]), int(W), int(H), int(P)]

#Tracklet for entity
def tracklet(entity):
    return [entity["classID"], entity["entityID"]] + [x for sublist in entity["history"] for x in sublist]
    
#All tracklets for the entities (excluding not spawned and terminated ones according to current time t, and out of screen ones)
def entitiesAtTime(entities, t):
    return [x for x in entities if alive(x,t) and len(x["history"])==5]

#Simulation step for the entity (procedure, modifies entity)
def simulateEntity(entity, t):
    #If not alive currently, do nothing
    if not alive(entity, t): return
    #Movement of the entity
    ((x,y), v, a) = (entity["location"], entity["speed"], entity["angle"])
    entity["location"] = (x+cos(a)*v, y+sin(a)*v)
    #Add current tracklet point to history, trimmed to 5 at most
    entity["history"] = (entity["history"] + [trackletPoint(entity)])[-5:]
    #Change angle and speed in case that it reached a relevant location:
    for change in entity["behavior"]:
        if similarLocation(entity["location"], change["location"], change["tolerance"]):
            print("t=" + str(t) + ": changeAngleAndSpeed entity" + str(entity["entityID"]))
            if change["angle"] != None:
                entity["angle"] = change["angle"]
            if change["speed"] != None:
                entity["speed"] = change["speed"]

#Simulation step for entities (procedure, modifies entities)
def simulateEntities(entities, t):
    for x in entities:
        simulateEntity(x, t)

#Utility to support mixing scenarios in a script
def AddToEntities(entities, entitiesToAdd, spawnTimeOffset, change_direction=True, max_amount=9999, offsetx=0, offsety=0):
    k=0
    random.shuffle(entitiesToAdd)
    for ent_ in entitiesToAdd:
        ent = deepcopy(ent_)
        ent["spawnTime"] += spawnTimeOffset
        ent["location"] = (ent["location"][0]+offsetx, ent["location"][1]+offsety)
        if not change_direction:
            ent["behavior"] = []
        entities.append(ent)
        k+=1
        if k >= max_amount:
            return
