# -*- coding: utf8 -*-
"""
------------------------------------------------
   "LIABILITY INSURANCE CHECKER" - PyGameApp.py
------------------------------------------------
Class structure in File:

[CONFIG and INIT]
    * InitialConfigVariablePreparation - preparation of initial variables
    * BaseConf - basic configuration
    * ViewConf(BaseConf) - front view configuration

[MAIN and VIEW]
    * App - Main class
    * FrontViewHandler - view handler

[THREADS]
    * UFGThread - get plate insurance info from UFG
    * ALPRThread - get plate number from cam img
    * CAMThread - capture camera img

"""
import sys
import os
import subprocess
import multiprocessing
import json
import glob
import shutil
import threading
import time as imported_time
from datetime import datetime

import pygame
from pygame import *
from pygame import camera
# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import cv2
import numpy

os.environ["SDL_FBDEV"] = "/dev/fb1"
pygame.init()

# Global controll, trigger, thread communication variables
ALPR, UFG = {"status": 0, "result": ""}, {"status": 0, "result": ""}
EXIT_FLAG = False
CAM_IMG = None
DEBUG = False


def debug_log(text):
    if DEBUG is True:
        print text


class InitialConfigVariablePreparation:
    """
    Prepare initial constan items
    "Helper Class" for BaseConf - basic configuration class
    (only for convenience)
    """

    def set_theme_object(self, normal, success, warning):
        """
        Prepare theme object
        """
        theme_object = {}
        for state_id, theme in enumerate([normal, success, warning]):
            theme_object_normal, theme_object_hover = {}, {}
            for theme_item_id, theme_item in enumerate(["shadow", "body", "line", "background", "txt"]):
                theme_object_normal.update({theme_item: theme[0][theme_item_id]})
                theme_object_hover.update({theme_item: theme[1][theme_item_id]})
            theme_object.update({state_id: [theme_object_normal, theme_object_hover]})
        return theme_object

    def set_folders(self, saved_data_folder_name, saved_cam_img_folder_name):
        """
        Set and create working directories
        """
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        saved_data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), saved_data_folder_name))
        camera_img_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), saved_cam_img_folder_name))
        for folder in [camera_img_folder, saved_data_folder, saved_data_folder + "/success", saved_data_folder + "/failed"]:
            if not os.path.exists(folder):
                os.makedirs(folder)
        return [saved_data_folder, camera_img_folder, root_dir]


class BaseConf:
    """
    Project basic settings:
    """
    caption = "LIABILITY INSURANCE CHECKER"  # Set the caption for the window.
    screen_size = (480, 320)
    background_color = pygame.Color("black")
    fps = 30  # Define max frame rate.
    cam_fps = 15
    ufg_time_interval = 1000 * 5  # 1000 = 1 sec - interval"s between plate"s
    alpr_time_interval = 1000 * 5  # 1000 = 1 sec - interval"s between plate"s
    save_processed_cam_img = False
    saved_data_folder_name = "saved_data"
    saved_cam_img_folder_name = "saved_cam_img"
    auto_img_capture = False  # If True automatic cam picture capturing is enabled Else Manual Capturing via click is ON
    auto_img_capture_interval = 10000
    save_all_ufg_request_results = False
    cam_res_x = 320
    cam_res_y = 240

    # prepare constant items based on settings
    set_var = InitialConfigVariablePreparation()
    saved_data_folder = set_var.set_folders(saved_data_folder_name, saved_cam_img_folder_name)[0]
    camera_img_folder = set_var.set_folders(saved_data_folder_name, saved_cam_img_folder_name)[1]


class ViewConf(BaseConf):
    """
    Front view settings:
    """
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 255)
    aqua = (51, 204, 255)
    azure = (0, 153, 255)
    aqua_dark = (10, 30, 70)
    cyan = (0, 255, 255)
    cyan_dark = (0, 105, 105)
    green = (0, 255, 0)
    green_dark = (0, 55, 0)
    forest = (34, 139, 34)
    lawn_green = (124, 252, 0)
    red = (200, 0, 0)
    red_dark = (110, 0, 0)
    orange_red = (255, 69, 0)
    maroon = (128, 0, 0)
    yellow = (255, 255, 0)
    orange = (255, 128, 0)
    yellow_mid = (195, 195, 0)
    firebrick = (255, 48, 48)
    crimson = (220, 20, 60)


    # [Themes][color settings for label and buttons in different states]
    # figure_element = ["shadow", "body", "line", "background", "txt"]
    normal = [[azure, aqua, cyan, black, white],  # normal state
              [cyan_dark, azure, aqua, cyan, black]]  # hover state

    success = [[green_dark, forest, lawn_green, black, white],  # normal state
               [green_dark, green, forest, lawn_green, black]]  # hover state

    warning = [[orange_red, red, yellow_mid, black, white],  # normal state
               [maroon, red, orange, firebrick, black]]  # hover state

    # set prepared theme object based on color settings
    theme_object = BaseConf.set_var.set_theme_object(normal, success, warning)

    # Various view compositions => [show_cam, show_info, label_size]
    view_compositions = {0: [True, True, 245],  # Show cam - in bigger label.
                         1: [True, False, 165],  # Show cam - in taller label.
                         2: [False, True, 245],  # Don't show cam , show ufg result.
                         3: [False, False, 165]}  # Don't show cam , show only plate.


class App(object):
    """
    This is the main class for our application.
    It manages our event and app loops.
    """
    config = BaseConf()

    def __init__(self, plate=None):
        """
        Get a reference to the screen (created in main);
        define and init necessary: attributes; Classes; Variables;
        """

        # PyGame init
        self.screen = pygame.display.get_surface()  # Get reference to the display.
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()  # Create a clock to restrict frame rate.
        self.keys = pygame.key.get_pressed()  # All the keys currently held.

        # Variables
        self.plate = "no plate" if plate is None else plate
        self.result = None
        self.background_rect, self.cam_display_rect = None, None

        self.parsed = {"img": "", "plate": ""}  # currently parsed cam img and plate

        # Classes
        self.front_view_handler = FrontViewHandler(self.plate)

        # Queues
        self.queues = {"alpr": [], "ufg": []}

        # Events - Interval triggers 
        self.check_next = {"ufg": [True, pygame.USEREVENT + 1],
                           "alpr": [True, pygame.USEREVENT + 2],
                           "capture": [True, pygame.USEREVENT + 3]}
        # Camera
        self.run_camera_capture_thread()

    def run_camera_capture_thread(self):
        thread_cam = CAMThread()
        thread_cam.start()

    def save_current_cam_frame(self):
        """
        Add currently captured frame to proccessing queue
        """
        debug_log("SAVING CAPTURED IMG")
        time_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copyfile(self.config.saved_data_folder + "/currently_displayed.jpg",
                        self.config.camera_img_folder + "/" + time_str + ".jpg")

    def save_results(self, plate, result):
        """
        Save UFG request plate info result
        """
        self.front_view_handler.current_figure_state[2] = 1
        save_to_file = open(self.config.saved_data_folder + "/" + plate + "_saved", "w")
        try:
            save_to_file.write(result)
        except UnicodeEncodeError:
            save_to_file.write(result.encode("UTF8"))
        except TypeError as e:
            debug_log("Nothing to save!")
        save_to_file.close()

    def alpr_controller(self):
        """
        - Check current ALPR class processing status
        - if 0 -> 'ready to recognize' -> Must turn on -> check queue -> start processing thread
        - if 1 -> 'recognize in progress' -> do nothing.
        - if 2 -> 'recognize finished  -> process result, if success put to UFG queue
        - start 'self trigger' interval event.
        """
        global ALPR

        def _start_alpr_recognizing_thread(camera_img):
            thread_alpr = ALPRThread(camera_img)
            thread_alpr.start()
            debug_log("-[ALPR recognizing thread started]-")

        def _start_next_event_interval():
            debug_log("-[starting ALPR next event interval]-")
            pygame.time.set_timer(self.check_next["alpr"][1], self.config.alpr_time_interval)
            self.check_next["alpr"][0] = False

        def _update_image_recognizing_queue():
            img_to_recognize = []
            os.chdir(self.config.camera_img_folder)
            for img in glob.glob("*.jpg"):
                img_to_recognize.append(img)
            self.queues["alpr"] = img_to_recognize
            self.front_view_handler.update_queues([len(self.queues["alpr"]), len(self.queues["ufg"])])
            if len(img_to_recognize) > 0:
                debug_log("-[ALPR Queue Len: " + str(len(self.queues["alpr"])) + " -> start recognize next cam img]-")
                return True
            else:
                debug_log("-[ALPR Queue Empty!]-")
                return False

        def _recognize_image():
            next_img = self.config.camera_img_folder + "/" + self.queues["alpr"].pop()
            self.parsed["img"] = next_img
            _start_alpr_recognizing_thread(next_img)

        def _get_recognaizing_result():
            if len(ALPR["result"]) > 0 and ALPR["result"] != "failed":
                _move_recognized_img(self.parsed["img"], True)
                self.queues["ufg"].append(ALPR["result"])
                self.front_view_handler.update_queues([len(self.queues["alpr"]), len(self.queues["ufg"])])
            else:
                _move_recognized_img(self.parsed["img"], False)

        def _move_recognized_img(parsed_img, status):
            # pass
            if self.config.save_processed_cam_img is False:
                os.remove(parsed_img)
            elif status is True:
                shutil.move(parsed_img, self.config.saved_data_folder + "/success" + parsed_img[parsed_img.rfind("/"):])
            else:
                shutil.move(parsed_img, self.config.saved_data_folder + "/failed" + parsed_img[parsed_img.rfind("/"):])

        if ALPR["status"] is 0:
            debug_log("-[ALPR status 0 -> ready to recognize -> check if queue not empty...]-")
            if _update_image_recognizing_queue():
                _recognize_image()
        elif ALPR["status"] is 1:
            debug_log("-[ALPR status 1 -> recognize progress -> wait for results...]-")
        elif ALPR["status"] is 2:
            debug_log("-[ALPR status 2 -> recognize finished -> processing result -> " + str(ALPR["result"]) + " ]")
            _get_recognaizing_result()
            ALPR["status"], ALPR["result"], self.parsed["img"] = 0, "", ""
        _start_next_event_interval()

    def ufg_controller(self):
        """
        - Check current UFG class processing status
        - if 0 -> 'ready to request' -> Must turn on -> check queue -> start processing thread  # TODO check net connection
        - if 1 -> 'requesting in progress' -> do nothing.
        - if 2 -> 'requesting finished  -> process result,
        - start 'self trigger' interval event.
        """
        global UFG

        def _start_ufg_requesting_thread(plate):
            thread_ufg = UFGThread(plate)
            thread_ufg.start()
            debug_log("-[UFG requesting thread started]-")

        def _start_next_event_interval():
            debug_log("-[starting UFG next event interval]-")
            pygame.time.set_timer(self.check_next["ufg"][1], self.config.ufg_time_interval)
            self.check_next["ufg"][0] = False

        def _request_ufg():
            next_plate = self.queues["ufg"].pop()
            self.parsed["plate"] = next_plate
            _start_ufg_requesting_thread(next_plate)

        def _process_ufg_result(plate, result):
            self.front_view_handler.update_plate(plate, result)
            if self.config.save_all_ufg_request_results:
                self.save_results(plate, result)

        if UFG["status"] is 0:
            debug_log("-[UFG status 0 -> ready to request -> check if queue not empty...]-")
            self.front_view_handler.update_queues([len(self.queues["alpr"]), len(self.queues["ufg"])])
            if len(self.queues["ufg"]) > 0:
                _request_ufg()
            else:
                debug_log("-[UFG empty queue]-")
        elif UFG["status"] is 1:
            debug_log("-[UFG status 1 -> requesting progress -> wait for results...]-")
            self.front_view_handler.update_plate(self.parsed["plate"], "processing")
        elif UFG["status"] is 2:
            debug_log("-[UFG status 2 -> requesting finished -> processing result -> " + str(UFG["result"]) + " ]")
            _process_ufg_result(self.parsed["plate"], UFG["result"])
            UFG["status"], UFG["result"], self.parsed["plate"] = 0, "", ""
        _start_next_event_interval()

    def check_intervals(self):
        """
        trigger event's after interval runs out.
        """
        if self.check_next["alpr"][0] is True:
            self.alpr_controller()

        if self.check_next["ufg"][0] is True:
            self.ufg_controller()

        if self.check_next["capture"][0] and self.config.auto_img_capture:
            pygame.time.set_timer(self.check_next["capture"][1], self.config.auto_img_capture_interval)
            self.check_next["capture"][0] = False
            self.save_current_cam_frame()

    def event_loop(self):
        """
        Our event loop; called once every frame.  Only things relevant to
        processing specific events should be here.  It should not
        contain any drawing/rendering code.
        """
        global EXIT_FLAG

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                self.front_view_handler.cursor_motion(event.pos)

            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                EXIT_FLAG = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_result = self.front_view_handler.click_on_figure_handler(event.pos)
                if click_result is "exit":
                    EXIT_FLAG = True
                elif click_result == "save":
                    self.save_results(self.plate, self.result)
                elif click_result == "capture":
                    self.save_current_cam_frame()

            elif event.type == self.check_next["ufg"][1]:
                self.check_next["ufg"][0] = True
                pygame.time.set_timer(self.check_next["ufg"][1], 0)
                debug_log('-event.type == self.check_next["ufg"][1]:')

            elif event.type == self.check_next["alpr"][1]:
                self.check_next["alpr"][0] = True
                pygame.time.set_timer(self.check_next["alpr"][1], 0)
                debug_log('-event.type == self.check_next["alpr"][1]:')

            elif event.type == self.check_next["capture"][1]:
                self.check_next["capture"][0] = True
                pygame.time.set_timer(self.check_next["capture"][1], 0)

    def render(self):
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(self.config.background_color)

        self.front_view_handler.update_label()
        pygame.display.update()

    def main_loop(self):
        """
        Main loop. It calls the event loop; updates the display;
        restricts the framerate; and loops.
        """
        global EXIT_FLAG
        while not EXIT_FLAG:
            self.event_loop()  # Run the event loop every frame.
            self.check_intervals()
            self.render()
            self.clock.tick(self.config.fps)  # Restrict frame rate of program.
            pygame.display.flip()


class FrontViewHandler(object):
    """
    FrontEnd display and event handler class
    """
    config = ViewConf()

    def __init__(self, plate):
        """
        figures = [0:label_area, 1:button_left, 2:button_mid, 3:button_right]
        """
        self.plate = plate
        self.result = ""
        self.screen = pygame.display.get_surface()
        self.current_figure_state = [0, 0, 0, 0]  # Current figure sate > 0:normal, 1:success, 2:warning
        self.cursor_on_figure = [False, False, False, False]  # Cursor position on figure flags
        self.click_on_figure = [False, False, False, False]  # Click on figure
        self.style = {"round": True, "frame": False}  # Corner rounding and frame style
        self.current_view = 0  # current view composition flag

        self.queues_len = {"alpr": 0, "ufg": 0, "success": 0, "failed": 0, "last_plate": ""}

        self.rect_obj = {}  # all figure rectangles
        self.update_figure_sizes()

    def update_label(self):
        """
        updates label height and cam image
        """
        self.update_figure_sizes()
        self.draw_figures()
        self.set_text()

    def update_queues(self, queues):
        self.queues_len["alpr"] = queues[0]
        self.queues_len["ufg"] = queues[1]

    def update_plate(self, plate, result):
        """
        updates current plate and result
        """
        debug_log("UPDATE FRONT PANEL! plate:" + str(plate) + " result: " + str(result))
        self.plate = plate
        self.result = result

    def update_figure_sizes(self):
        """
        Updates figure sizes after resize
        """
        label_height = self.config.view_compositions[self.current_view][2]
        button_pos_y = label_height + 5
        button_height = 310 - label_height
        self.rect_obj = {0: [2, 0, 477, label_height],  # top label
                         1: [2, button_pos_y, 155, button_height],  # left button
                         2: [162, button_pos_y, 155, button_height],  # mid button
                         3: [322, button_pos_y, 155, button_height]}  # result label

    def cursor_motion(self, pos):
        """
        This function is called from the event loop to check if a mouse move occurs
        """

        def _figure_hover(pos):
            """
            This function is called if cursor overlaps with a figure rect.
            """
            for number, figure in enumerate(self.rect_obj):
                if pygame.Rect(self.rect_obj[number]).collidepoint(pos):
                    self.cursor_on_figure[number] = True
                    pygame.mouse.get_rel()
                else:
                    self.cursor_on_figure[number] = False

        _figure_hover(pos)

    def click_on_figure_handler(self, pos):
        """
        This function is called from the event loop to check if a click
        overlaps with the figure rect
        """

        def _invert_state(state_variable):
            return False if state_variable is True else True

        def _round_figure_corners():
            """
            round button corners and switch styles(increase or decrease border width)
            """
            self.style["round"] = _invert_state(self.style["round"])
            if self.style["round"] is True:
                self.style["frame"] = _invert_state(self.style["frame"])

        def _switch_view_composition():
            """
            Switch between view compositions
            """
            self.current_view += 1 if self.current_view != 3 else -3
            self.update_figure_sizes()

        for number, figure in enumerate(self.rect_obj):

            # Clicked EXIT button.
            if pygame.Rect(self.rect_obj[3]).collidepoint(pos):
                return "exit"

            # Show/Hide plate info.
            elif pygame.Rect(self.rect_obj[1]).collidepoint(pos):
                _switch_view_composition()
                break

            # Save current results to file trigger
            elif pygame.Rect(self.rect_obj[2]).collidepoint(pos):
                return "save"

            # Set rounded or square figures trigger
            elif pygame.Rect(self.rect_obj[0]).collidepoint(pos):
                _round_figure_corners()
                if self.config.view_compositions[self.current_view][0] is True:
                    return "capture"
            else:
                self.click_on_figure[number] = False

    def draw_figures(self):
        """
        Drawing buttons and top label with hover handling.
        """

        def _rounded_rect(surface, rect, color, radius=0.4):
            """
            surface : destination
            rect    : rectangle
            color   : gb or rgba
            radius  : 0 <= radius <= 1
            """
            rect = Rect(rect)
            color = Color(*color)
            alpha = color.a
            color.a = 0
            pos = rect.topleft
            rect.topleft = 0, 0
            rectangle = Surface(rect.size, SRCALPHA)
            circle = Surface([min(rect.size) * 3] * 2, SRCALPHA)
            draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
            circle = transform.scale(circle, [int(min(rect.size) * radius)] * 2)
            radius = rectangle.blit(circle, (0, 0))
            radius.bottomright = rect.bottomright
            rectangle.blit(circle, radius)
            radius.topright = rect.topright
            rectangle.blit(circle, radius)
            radius.bottomleft = rect.bottomleft
            rectangle.blit(circle, radius)
            rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
            rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))
            rectangle.fill(color, special_flags=BLEND_RGBA_MAX)
            rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)
            return surface.blit(rectangle, pos)

        def _draw(pos_x1, pos_y1, pos_x2, pos_y2, theme_item, figure_id):
            state = self.current_figure_state[fig]
            hover = self.cursor_on_figure[fig]
            color_theme = self.config.theme_object[state][1] if hover is True else self.config.theme_object[state][0]
            if self.style["round"] is False or figure_id == 0:
                pygame.draw.rect(self.screen, color_theme[theme_item], (pos_x1, pos_y1, pos_x2, pos_y2))
            else:
                _rounded_rect(self.screen, (pos_x1, pos_y1, pos_x2, pos_y2), color_theme[theme_item], 0.5)

        def _draw_camera(pos_x1, pos_y1, pos_x2, pos_y2, style):
            global CAM_IMG
            if CAM_IMG is not None:
                self.background_rect = CAM_IMG
                self.cam_display_rect = [450 - 2 * style, self.rect_obj[0][3] - 23 - 2 * style]
                image = pygame.transform.smoothscale(self.background_rect, self.cam_display_rect)
                img_position = (pos_x1, pos_y1, pos_x2 - 2 * style, pos_y2 - 2 * style)
                self.screen.blit(image, img_position)

        # figure styling params:
        style = 0 if self.style["frame"] is False else 6
        add = 5 + style
        rem = 2 * add

        # Drawing loop for all figures
        for fig, x in enumerate([0, 5, 165, 325]):  # x axis start positions
            if fig is 0:  # Top Label
                _draw(4, 2, 475, self.rect_obj[0][3], "shadow", 0)
                _draw(2, 0, 475, self.rect_obj[0][3], "line", 0)
                _draw(3, 0, 472, self.rect_obj[0][3] - 1, "body", 0)
                _draw(8 + add, 5 + add, 462 - rem, self.rect_obj[0][3] - 11 - rem, "line", 0)
                _draw(9 + add, 6 + add, 461 - rem, self.rect_obj[0][3] - 12 - rem, "shadow", 0)
                _draw(10 + add, 7 + add, 460 - rem, self.rect_obj[0][3] - 13 - rem, "background", 0)
                if self.config.view_compositions[self.current_view][0] is True:
                    _draw_camera(10 + add, 7 + add, 460 - rem, self.rect_obj[0][3] - 13 - rem, style)

            else:  # Buttons
                _draw(x + 1, self.rect_obj[1][1] + 1, 150, self.rect_obj[1][3], "shadow", fig)
                _draw(x, self.rect_obj[1][1] + 1, 148, self.rect_obj[1][3] - 2, "line", fig)
                _draw(x + 1, self.rect_obj[1][1] + 2, 146, self.rect_obj[1][3] - 4, "body", fig)
                _draw(x + style + 9, self.rect_obj[1][1] + style + 10, 130, self.rect_obj[1][3] - 20, "line", fig)
                _draw(x + style + 10, self.rect_obj[1][1] + style + 11, 129, self.rect_obj[1][3] - 21, "shadow", fig)
                _draw(x + style + 11, self.rect_obj[1][1] + style + 12, 128, self.rect_obj[1][3] - 22, "background", fig)

    def set_text(self):
        """
        Draw text for: Label, Buttons, Result
        """

        def _set_font(text, size, color):
            font_declare = pygame.font.SysFont("Calibri", size, True, False)
            set_font = font_declare.render(text, True, color)
            return set_font

        def _text_color(text_id):  # set text color from theme
            state = self.current_figure_state[text_id]
            hover = self.cursor_on_figure[text_id]
            color_theme = self.config.theme_object[state][1] if hover is True else self.config.theme_object[state][0]
            return color_theme["txt"]

        def _shadow_color(text_id):  # set text shadow color from theme
            state = self.current_figure_state[text_id]
            hover = self.cursor_on_figure[text_id]
            color_theme = self.config.theme_object[state][1] if hover is True else self.config.theme_object[state][0]
            return color_theme["shadow"]

        def _draw_text(text, size, position, figure_id):
            shadow_x = position[0] + 1 if size < 31 else position[0] + 2
            shadow_y = position[1] + 1 if size < 31 else position[1] + 2
            self.screen.blit(_set_font(text, size, self.config.white), [position[0] - 1, position[1]])
            self.screen.blit(_set_font(text, size, _shadow_color(figure_id)), [shadow_x, shadow_y])
            self.screen.blit(_set_font(text, size, _text_color(figure_id)), [position[0], position[1]])

        def _draw_result_info(result_obj, s):
            """
            result_obj - decoded json object
            s - stylization pixel rate
            """
            _draw_text(u"      [" + str(self.plate) + u"] " + result_obj[u"Dla pojazdu"], 27, [15 + s, 15 + s], 0)
            if self.config.view_compositions[self.current_view][0] is False:
                _draw_text(7 * u" " + result_obj[u"Cel zapytania"], 20, [15 + s, 45 + s], 0)
                _draw_text(u" " + result_obj[u"Zapytanie"][1:], 18, [15 + s, 75 + s], 0)
                _draw_text(u" Polisa:" + result_obj[u"Polisa"], 20, [15 + s, 105 + s], 0)
                _draw_text(u" " + result_obj[u"Zakład odpowiedzialny"], 18, [15 + s, 135 + s], 0)
                _draw_text(u" " + result_obj[u"Adres"], 20, [15 + s, 165 + s], 0)
                temp_txt = result_obj[u"Treść zapytania"]
                line = u"   Pojazd " + temp_txt[35:temp_txt.strip().find("OC") + 2].strip()
                _draw_text(line, 18, [15 + s, 190 + s], 0)

        def _append_result_stats(state):
            if self.plate != self.queues_len["last_plate"]:
                self.queues_len["last_plate"] = self.plate
                self.queues_len[state] += 1

        def _set_plate_state():
            """
            updates plate state (normal, success, failed)
            """
            if self.result == "processing":
                self.current_figure_state[0] = 0  # normal
                return 0
            elif self.result == "failed" or len(self.result) < 1:  # failed
                self.current_figure_state[0] = 2
                _append_result_stats("failed")
                return 2
            else:
                self.current_figure_state[0] = 1  # success
                _append_result_stats("success")
                return 1

        def _draw_queue_counts():
            """
            Draw Queue counts for alpr, ufg, success, failed
            """
            queues_list = [[str(self.queues_len["alpr"]), 20, self.config.white],
                           [str(self.queues_len["ufg"]), 50, self.config.blue],
                           [str(self.queues_len["success"]), 80, self.config.green],
                           [str(self.queues_len["failed"]), 110, self.config.red]]
            font_size = 30
            for queue in queues_list:
                shadow_x = 440 + 1
                shadow_y = queue[1] + 1
                self.screen.blit(_set_font(queue[0], font_size, queue[2]), [439, queue[1]])
                self.screen.blit(_set_font(queue[0], font_size, queue[2]), [shadow_x, shadow_y])
                self.screen.blit(_set_font(queue[0], font_size, queue[2]), [440, queue[1]])

        state = _set_plate_state()
        style = 0 if self.style["frame"] is False else 6
        plate_size = 110 if self.config.view_compositions[self.current_view][0] is False else 40
        if self.config.view_compositions[self.current_view][1] is False:
            _draw_text("SHOW", 40, [35 + style, 207 + style], 1)
            if self.current_view == 3:
                _draw_text("CAMERA", 31, [32 + style, 256 + style], 1)
            else:
                _draw_text("INSURANCE", 27, [24 + style, 256 + style], 1)
            _draw_text("SAVE", 45, [197 + style, 205 + style], 2)
            _draw_text("RESULTS", 31, [189 + style, 255 + style], 2)
            _draw_text("EXIT", 45, [362 + style, 205 + style], 3)
            _draw_text("PROGRAM", 31, [346 + style, 255 + style], 3)
            _draw_text(self.plate, plate_size, [30 + style, 30 + style], 0)
        else:
            _draw_text("VIEW", 45, [40 + style, 265 + style], 1)
            _draw_text("SAVE", 45, [197 + style, 265 + style], 2)
            _draw_text("EXIT", 45, [362 + style, 265 + style], 3)

            if state is 1:
                result_obj = self.result
                _draw_result_info(result_obj, style)
            elif state is 2:
                _draw_text(u"  no results found!", 50, [25, 25], 0)
            else:
                _draw_text(u"  processing...", 50, [25, 25], 0)

        _draw_queue_counts()


class ALPRThread(threading.Thread):
    def __init__(self, camera_img):
        threading.Thread.__init__(self)
        self.name = camera_img[camera_img.rfind('/'):]
        self.camera_img = camera_img

    def run(self):
        debug_log("[THREAD ALPR]> Starting " + self.name)
        self.process_alpr(self.camera_img, self.name)
        debug_log("[THREAD ALPR]> Exiting " + self.name)

    def process_alpr(self, camera_img, thread_name):
        global ALPR, EXIT_FLAG
        finished_flag = False
        ALPR["status"] = 1

        while not finished_flag:
            if EXIT_FLAG:
                thread_name.exit()
            debug_log("[THREAD ALPR]>  %s: %s" % (thread_name, imported_time.ctime(imported_time.time())))
            command = ["sudo", "alpr", "-c", "eu", "-n", "1", "-j", camera_img, "2>/dev/null", "|", "sudo", "python", "load_json.py"]
            output = subprocess.Popen(command, cwd="/home/theta/", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      shell=False)
            stdout, stderr = output.communicate()
            json_result = json.loads(stdout.strip())
            try:
                ALPR["result"] = json_result["results"][0]["candidates"][0]["plate"]
                debug_log("[THREAD ALPR]> RESULT: " + ALPR["result"])
            except Exception as e:
                ALPR["result"] = "failed"
                debug_log(str(stderr) + str(e))
                pass
            ALPR["status"] = 2
            finished_flag = True


class UFGThread(threading.Thread):
    def __init__(self, plate):
        threading.Thread.__init__(self)
        self.name = plate

    def run(self):
        debug_log("[THREAD UFG]> Starting " + self.name)
        self.process_ufg(self.name)
        debug_log("[THREAD UFG]> Exiting " + self.name)

    def process_ufg(self, plate):
        global UFG, EXIT_FLAG
        finished_flag = False
        UFG["status"] = 1

        while not finished_flag:
            if EXIT_FLAG:
                plate.exit()

            debug_log("[THREAD UFG]>  %s: %s" % (plate, imported_time.ctime(imported_time.time())))
            output = subprocess.Popen(["python", "UFGRequestor.py", plate, "-d"],
                                      cwd="/home/theta/alpr-ufg",
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
            stdout, stderr = output.communicate()
            UFG["result"] = json.loads(stdout[stdout.find("{"):stdout.find("}") + 1]) if stdout.find("}") > 0 else "failed"
            UFG["status"] = 2
            finished_flag = True


class CAMThread(threading.Thread):
    conf = BaseConf()

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "CamThread"

    def run(self):
        debug_log("[THREAD CAM]> Starting " + self.name)
        self.process_cam(self.name)
        debug_log("[THREAD CAM]> Exiting " + self.name)

    def process_cam(self, thread_name):
        finished_flag = False
        cam = PiCamera()
        cam.resolution = (self.conf.cam_res_x, self.conf.cam_res_y)
        cam.framerate = self.conf.cam_fps
        raw_capture = PiRGBArray(cam, size=(self.conf.cam_res_x, self.conf.cam_res_y))

        def _resize(image):
            r = 320.0 / image.shape[1]
            dim = (100, int(image.shape[0] * r))
            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.conf.saved_data_folder + "/currently_displayed_resized.jpg", resized)

        def _get_cam_img():
            global CAM_IMG, EXIT_FLAG
            for frame in cam.capture_continuous(raw_capture, format="bgr", use_video_port=True):
                image_from_cam = frame.array
                cv2.imwrite(self.conf.saved_data_folder + "/currently_displayed.jpg", image_from_cam)
                # _resize(image_from_cam)
                # cv2.waitKey(0)
                raw_capture.truncate(0)
                CAM_IMG = pygame.image.load(self.conf.saved_data_folder + "/currently_displayed.jpg")
                break

        while not finished_flag:
            if EXIT_FLAG:
                self.name.exit()
            _get_cam_img()


def main(plate=None):
    """
    Prepare our environment, create a display, and start the program.
    """
    config = BaseConf()
    pygame.init()  # Initialize Pygame.
    pygame.display.set_caption(config.caption)  # Set the caption for the window.
    pygame.display.set_mode(config.screen_size)  # Prepare the screen.
    App(plate).main_loop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
