#!/usr/bin/env python
# coding=utf-8

import datetime
import os
import shutil
import sys

import cmd2
from cmd2 import style, fg, bg

from TimeTable import TimeTable

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename


table = TimeTable()
base_path = "C:/Users/Jonas Biba/Documents/PrincessCarolin/Notes"


entry_template = """
<div class="single-blog">
        <a href="{0}"><h3>{1}</h3></a>
        <div class="blog-info">
            <ul>
                <li><a href="">{2}</a></li>
                <li><a href="">{3}</a></li>
                <!--<li><a href="">10 Comments</a></li>-->
            </ul>

            <div class="read-more pull-right">
                <a href="{0}" class="btn btn-readmore">Site</a>
            </div>

        </div>
</div>
"""


class CmdLineApp(cmd2.Cmd):
    # print all past classes with titles
    """ Example cmd2 application. """

    # Setting this true makes it run a shell command if a cmd2/cmd command doesn't exist
    default_to_shell = True

    def __init__(self):
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        # shortcuts.update({'&': 'speak'})

        # Prints an intro banner once upon application startup
        self.intro = style("How is my favorite client doing? I am here to manage all your notes!", fg=fg.red, bg=bg.white, bold=True)

        # Show this as the prompt when asking for input
        self.prompt = 'P.C.> '

        self.current_notes = ""

        super().__init__(multiline_commands=['orate'], shortcuts=shortcuts)

        # Make maxrepeats settable at runtime
        # self.add_settable(cmd2.Settable('maxrepeats', int, 'max repetitions for speak command', None))

    make_parser = cmd2.Cmd2ArgumentParser()
    make_parser.add_argument('note', nargs='+', help='course date topic?')

    @cmd2.with_argparser(make_parser)
    def do_make(self, args):
        """Create notes for the class you are in right now based on your schedule."""
        if len(args.note) == 4:
            course_path = base_path + "/" + args.note[1]
            if not os.path.isdir(course_path):
                shutil.copytree(base_path + "/templates/template_course", course_path)
                with open(base_path + "/sidebar.html", "a") as sidebar:
                    sidebar.write("\n" + "<a href='" + args.note[1] + "/course.html" + "'>" + args.note[1] + "</a>")
                # create course index.html
            # os.chdir(course_path)
            class_path = args.note[2]
            if os.path.isdir(class_path):
                self.poutput("You already created notes for this class. "
                             "Activate the environment with start {COURSE}/{DATE}")
            else:
                shutil.copytree(base_path + "/templates/template_class", course_path + "/" + class_path)
                self.current_notes = args.note[1] + "/" + class_path
                # add entry in index.html
                with open(course_path + "/notes_in_course.html", "a") as notes_in_course:
                    # data = notes_in_course.readlines()
                    notes_in_course.write("\n" + entry_template.format(class_path + "/index.html",
                                                      args.note[3] or "Class of " + args.note[2],
                                                      args.note[1],
                                                      args.note[2]))
                with open(base_path + "/notes.html", "a") as notes:
                    # data = notes_in_course.readlines()
                    notes.write("\n" + entry_template.format(class_path + "/index.html",
                                                                       args.note[3] or "Class of " + args.note[2],
                                                                       args.note[1],
                                                                       args.note[2]))
                    # notes_in_course.writelines(data)
                self.poutput("Notes created. You can start taking notes by using the command: start!")
        elif 1 < len(args.note) < 4:
            self.poutput("You need to specify course, date and topic.")
        else:
            course_name = table.get_course()
            if course_name == "":
                self.poutput("You are not in a class right now. \n If you want to create some notes anyway, "
                             "you need to specify course, date and topic.")
            else:
                course_path = base_path + "/" + course_name
                if not os.path.isdir(course_path):
                    shutil.copytree(base_path + "/templates/template_course", course_path)
                    with open(base_path + "/sidebar.html", "a") as sidebar:
                        sidebar.write("\n" + "<a href='" + course_name + "/course.html" + "'>" + course_name + "</a>")
                    # create course index.html
                # os.chdir(course_path)
                class_path = datetime.datetime.now().isoformat().split("T")[0]
                if os.path.isdir(class_path):
                    self.poutput("You already created notes for this class. "
                                 "Activate the environment with start {COURSE}/{DATE}")
                else:
                    shutil.copytree(base_path + "/templates/template_class", course_path + "/" + class_path)
                    self.current_notes = course_name + "/" + class_path
                    # add entry in index.html
                    topic = input("Enter the topic of the class: ")
                    with open(base_path + "/" + course_name + "/notes_in_course.html", "a") as notes_in_course:
                        notes_in_course.write("\n" + entry_template.format(class_path + "/index.html",
                                                                           topic or "Class of " + class_path,
                                                          course_name,
                                                          class_path))
                    with open(base_path + "/notes.html", "a") as notes:
                        notes.write("\n" + entry_template.format(class_path + "/index.html",
                                                                 topic or "Class of " + class_path,
                                                                           course_name,
                                                                           class_path))
                    self.poutput("Notes created. You can start taking notes by using the command: start!")

    def do_start(self):
        pass

    def do_stop(self):
        self.prompt = "P.C.> "
        self.current_notes = ""

    def do_add(self):
        if self.current_notes == "":
            self.poutput("Oh fish! You have to start making notes before you can add an asset.")
        else:
            Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
            shutil.copyfile(filename, "assets/" + filename.split("/")[-1])
            self.poutput("Added {0} to the assets.".format(filename))

    def do_update(self):
        self.poutput("Updating the github repo with all the changes you made.")
        os.popen("git -C Notes/ add .")
        os.popen("git -C Notes/ commit -m \"Notes added on {0}\"".format(datetime.datetime.now().isoformat()))
        os.popen("git -C Notes/ branch -M main")
        os.popen("git -C Notes/ push -u origin main")

        os.popen("git -C Notes/ checkout gh-pages")
        os.popen("git -C Notes/ rebase master")
        os.popen("git -C Notes/ push origin gh-pages")
        os.popen("git -C Notes/ checkout master")
        self.poutput("Update done!")

    def do_title(self):
        pass


if __name__ == '__main__':
    app = CmdLineApp()
    sys.exit(app.cmdloop())
