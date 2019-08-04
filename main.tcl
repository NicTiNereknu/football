#############################################################################
# Generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#  Jul 23, 2019 11:02:46 PM CEST  platform: Windows NT
set vTcl(timestamp) ""


if {!$vTcl(borrow)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #ececec
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(active_menu_fg) #000000
}

#################################
#LIBRARY PROCEDURES
#


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top42
    global vTcl
    set base $vTcl(btop)
    if {$base == ""} {
        set base .top42
    }
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# GENERATED GUI PROCEDURES
#

proc vTclWindow.top42 {base} {
    if {$base == ""} {
        set base .top42
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background {#d9d9d9} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 519x565+533+80
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1684 1031
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "New Toplevel"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    button $top.but43 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text Button 
    vTcl:DefineAlias "$top.but43" "Button1" vTcl:WidgetProc "Toplevel1" 1
    bind $top.but43 <Button-1> {
        lambda e: btnButton1_Click(e)
    }
    button $top.but44 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text {Save Edges State} 
    vTcl:DefineAlias "$top.but44" "btnSaveEdgesState" vTcl:WidgetProc "Toplevel1" 1
    bind $top.but44 <Button-1> {
        lambda e: btnSaveEdgesState_Click(e)
    }
    canvas $top.can45 \
        -background {#d9d9d9} -borderwidth 2 -closeenough 1.0 -height 523 \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -relief ridge -selectbackground {#c4c4c4} \
        -selectforeground black -width 363 
    vTcl:DefineAlias "$top.can45" "Canvas1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab46 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Uplne Neco jineho} 
    vTcl:DefineAlias "$top.lab46" "Label1" vTcl:WidgetProc "Toplevel1" 1
    button $top.but45 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text {Load Edges State} 
    vTcl:DefineAlias "$top.but45" "btnLoadEdgesState" vTcl:WidgetProc "Toplevel1" 1
    bind $top.but45 <Button-1> {
        lambda e: btnLoadEdgesState_Click(e)
    }
    button $top.but46 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text {Play AI} 
    vTcl:DefineAlias "$top.but46" "btnPlayAI" vTcl:WidgetProc "Toplevel1" 1
    bind $top.but46 <Button-1> {
        lambda e: btnPlayAI_Click(e)
    }
    ttk::style configure Treeview.Heading -background #d9d9d9
    ttk::style configure Treeview.Heading -font "TkDefaultFont"
    vTcl::widgets::ttk::scrolledtreeview::CreateCmd $top.scr45 \
        -background {#d9d9d9} -height 15 -highlightbackground {#d9d9d9} \
        -highlightcolor black -width 30 
    vTcl:DefineAlias "$top.scr45" "trvPath" vTcl:WidgetProc "Toplevel1" 1
    bind $top.scr45 <<TreeviewSelect>> {
        lambda e: trvPath_Select(e)
    }
        .top42.scr45.01 configure -columns {}
        .top42.scr45.01 heading #0 -anchor center
        .top42.scr45.01 column #0 -width 421
        .top42.scr45.01 column #0 -minwidth 20
        .top42.scr45.01 column #0 -stretch 1
        .top42.scr45.01 column #0 -anchor w
    label $top.lab43 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text {AI paths} 
    vTcl:DefineAlias "$top.lab43" "Label2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent43 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black 
    vTcl:DefineAlias "$top.ent43" "txtNumberOfPathsToEndNodes" vTcl:WidgetProc "Toplevel1" 1
    button $top.but47 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text Set 
    vTcl:DefineAlias "$top.but47" "btnSetGameProperties" vTcl:WidgetProc "Toplevel1" 1
    bind $top.but47 <Button-1> {
        lambda e: btnSetGameProperties_OnClick(e)
    }
    button $top.but48 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font {-family {Segoe UI} -size 10 -weight bold} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text Play 
    vTcl:DefineAlias "$top.but48" "btnPlay" vTcl:WidgetProc "Toplevel1" 1
    bind $top.but48 <Button-1> {
        lambda e: btnPlay_OnClick(e)
    }
    canvas $top.can46 \
        -background {#d9d9d9} -borderwidth 2 -closeenough 1.0 -height 73 \
        -insertbackground black -relief ridge -selectbackground {#c4c4c4} \
        -selectforeground black -width 83 
    vTcl:DefineAlias "$top.can46" "canvasArrowUP" vTcl:WidgetProc "Toplevel1" 1
    canvas $top.can47 \
        -background {#d9d9d9} -borderwidth 2 -closeenough 1.0 -height 73 \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -relief ridge -selectbackground {#c4c4c4} \
        -selectforeground black -width 83 
    vTcl:DefineAlias "$top.can47" "canvasArrowDOWN" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab48 \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} 
    vTcl:DefineAlias "$top.lab48" "lblPlayer1Name" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab49 \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} 
    vTcl:DefineAlias "$top.lab49" "lblPlayer2Name" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.but43 \
        -in $top -x 50 -y 370 -anchor nw -bordermode ignore 
    place $top.but44 \
        -in $top -x 20 -y 490 -width 95 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.can45 \
        -in $top -x 130 -y 30 -width 363 -relwidth 0 -height 523 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab46 \
        -in $top -x 20 -y 400 -anchor nw -bordermode ignore 
    place $top.but45 \
        -in $top -x 20 -y 430 -width 107 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but46 \
        -in $top -x 20 -y 460 -width 97 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.scr45 \
        -in $top -x 500 -y 40 -width 440 -relwidth 0 -height 367 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab43 \
        -in $top -x 510 -y 30 -anchor nw -bordermode ignore 
    place $top.ent43 \
        -in $top -x 30 -y 530 -width 64 -relwidth 0 -height 20 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but47 \
        -in $top -x 21 -y 54 -width 83 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but48 \
        -in $top -x 21 -y 94 -width 83 -height 34 -anchor nw \
        -bordermode ignore 
    place $top.can46 \
        -in $top -x 60 -y 200 -width 48 -relwidth 0 -height 48 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.can47 \
        -in $top -x 60 -y 200 -width 48 -height 48 -anchor nw \
        -bordermode ignore 
    place $top.lab48 \
        -in $top -x 60 -y 180 -width 60 -relwidth 0 -anchor nw \
        -bordermode ignore 
    place $top.lab49 \
        -in $top -x 60 -y 250 -width 60 -relwidth 0 -anchor nw \
        -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top42 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}

