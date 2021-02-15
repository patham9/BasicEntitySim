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
import json
from copy import deepcopy
import os
import sys
import glob
from PIL import Image
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
cwd = os.getcwd()
os.chdir("./ona/misc/Python")
import ona.misc.Python.NAR as NAR
os.chdir(cwd)
from Encoder import *

FP_size = DefaultEntitySize #width of first person "virtual entity"
FP_speed = 30 #speed of first person entity
WIDTH = 1280
HEIGHT = 720
FP_speed = 0
s = 0 #how far we drove
showFOV = True

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)

#Simulate environment within time range, and send the tracklets
def enqueueSimulation(entities, t_start, t_end, visualize=True, gif=True, firstPersonSpeed = 0, startSimNarsese = "", startFrameNarsese="", endFrameNarsese="", endSimNarsese="", KnowledgeAtTime={}):
    global s
    FP_speed = firstPersonSpeed
    if visualize:
        if gif:
            os.system("rm *.png")
            os.system("rm *.gif")
        pygame.init()
        dis = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        myfont2 = pygame.font.SysFont('Comic Sans MS', 60)
        textsurfaces = {}
        for ent in entities:
            textsurfaces[ent["classID"]] = {}
            textsurfaces[ent["classID"]][ent["entityID"]] = myfont.render(ent["classID"] + str(ent["entityID"]), False, (0, 0, 0))
    for narsese in startSimNarsese.split("\n"):
        if len(narsese.strip()) > 0:
            NAR.AddInput(narsese)
    sys.stdout.flush()
    lastEntities = []
    for t in range(t_start, t_end):
        for narsese in startFrameNarsese.split("\n"):
            if len(narsese.strip()) > 0:
                NAR.AddInput(narsese)
        if t in KnowledgeAtTime:
            for narsese in KnowledgeAtTime[t].split("\n"):
                if len(narsese.strip()) > 0:
                    NAR.AddInput(narsese)
        s += FP_speed
        if visualize:
            dis.fill((0, 128, 0))
            #draw entities:
            for ent in entities:
                (px,py) = (ent["location"][0], ent["location"][1]+s)
                color = (255, 255, 0)
                if ent["color"] == "red":
                    color = (255,0,0)
                if ent["color"] == "green":
                    color = (0,255,0)
                if ent["color"] == "gray":
                    color = (128,128,128)
                szx = ent["width"]
                szy = ent["height"]
                pygame.draw.rect(dis, color, pygame.Rect(px-szx/2, py-szy/2, szx/2, szy/2))
                dis.blit(textsurfaces[ent["classID"]][ent["entityID"]],(px-szx/2, py-szy/2))
        simulateEntities(entities, t)
        entities_t = entitiesAtTime(entities, t)
        for narsese in narseseEncoder(entities_t, lastEntities, FP_size, FP_speed, WIDTH, HEIGHT, s):
            NAR.AddInput(narsese)
        lastEntities = deepcopy(entities_t)
        for narsese in endFrameNarsese.split("\n"):
            if len(narsese.strip()) > 0:
                executions = NAR.AddInput(narsese)["executions"]
                if len(executions) > 0:
                    op = executions[0]["operator"]
                    dis.blit(myfont2.render(op, False, (255, 0, 0)),(50, 10))
        if visualize:
            #draw fov:
            if showFOV:
                draw_polygon_alpha(dis, (128,128,255,128), [(WIDTH/2+DefaultEntitySize/2, HEIGHT), (WIDTH/2-DefaultEntitySize/2, HEIGHT), (0,HEIGHT/2), (WIDTH,HEIGHT/2)])
            if gif:
                pygame.image.save(dis, "screenshot" + ("0" if t<10 else "") + str(t) + ".png")
            pygame.display.flip()
            clock.tick(6)
        sys.stdout.flush()
    if visualize:
        pygame.quit()
    for narsese in endSimNarsese.split("\n"):
        if len(narsese.strip()) > 0:
            NAR.AddInput(narsese)
    if gif:
        frames = []
        imgs = sorted(glob.glob("*.png"))
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)
        # Save into a GIF file
        frames[0].save('animated.gif', format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=300, loop=0)
    sys.stdout.flush()
