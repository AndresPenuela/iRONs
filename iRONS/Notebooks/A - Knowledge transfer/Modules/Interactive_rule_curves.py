# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 18:26:41 2019

@author: ap18525
"""
import ipywidgets as widgets
import numpy as np
from bqplot import pyplot as plt
from bqplot import *
from bqplot.traits import *

def Interactive_rule_curve(policy_function, rule_curve,
                           s_min,s_max,
                           Qreg_rel_mean,Qreg_rel_min,Qreg_rel_max,
                           s_1,s_2):
    
    #Function to update the rule curve when changing the parameters with the sliders
    def update_rule_curve(s_1_0,s_1_1,s_1_2,s_1_3): 

        s_1         = [s_1_0,s_1_1,s_1_2,s_1_3] 
        s_2         = [s_1_0+s_2_inc,s_1_1+s_2_inc,s_1_2+s_2_inc,s_1_3+s_2_inc]
        
        param = {'curves':{'year_date'    : curve_dates,
                           'storage_frac' : [s_0,s_1,s_2,s_3]},
        
                 'rules' :{'year_date' : rule_dates,
                           'release'   : [u_0,u_1,u_2,u_3]}} # max release
        s_yday,r_yday = rule_curve(param)
        
        x0 = [s_min/s_max,   Qreg_rel_min]
        x1 = [s_1_0,         Qreg_rel_mean]
        x2 = [s_1_0+s_2_inc, Qreg_rel_mean]
        x3 = [s_max/s_max,   Qreg_rel_max]
        param_a = x0, x1, x2, x3
        u_frac_a = policy_function(param_a)

        x0 = [s_min/s_max,   Qreg_rel_min]
        x1 = [s_1_1,         Qreg_rel_mean]
        x2 = [s_1_1+s_2_inc, Qreg_rel_mean]
        x3 = [s_max/s_max,   Qreg_rel_max]
        param_b = x0, x1, x2, x3
        u_frac_b = policy_function(param_b)
        
        x0 = [s_min/s_max,   Qreg_rel_min]
        x1 = [s_1_2,         Qreg_rel_mean]
        x2 = [s_1_2+s_2_inc, Qreg_rel_mean]
        x3 = [s_max/s_max,   Qreg_rel_max]
        param_c = x0, x1, x2, x3
#        print(param_c)
        u_frac_c = policy_function(param_c) 
#        print(u_frac_c)
        
        return s_yday[1],s_yday[2], u_frac_a, u_frac_b, u_frac_c
    
    # Function to update the figures when changing the parameters with the sliders
    def update_figure(change):
        rule_curve_1.y = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[0]
        rule_curve_2.y = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[1]
        pol_func_a.y   = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[2]
        pol_func_b.y   = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[3]
        pol_func_c.y   = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[4]
    
    # Definition of the sliders (Points defining the curves) 
    curve_dates = ['1 Apr',    '1 Aug',    '1 Dec',    '31 Mar']
    s_1_0 = widgets.FloatSlider(min=0, max=0.705, value=s_1[0], step=0.01, 
                                description = 's1 at '+str(curve_dates[0])+': ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s_1_0.observe(update_figure,names = 'value')
    
    s_1_1 = widgets.FloatSlider(min=0, max=0.705, value=s_1[1], step=0.01, 
                                description = 's1 at '+str(curve_dates[1])+': ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s_1_1.observe(update_figure,names = 'value')
    
    s_1_2 = widgets.FloatSlider(min=0, max=0.705, value=s_1[2], step=0.01, 
                                description = 's1 at '+str(curve_dates[2])+': ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s_1_2.observe(update_figure,names = 'value')
    
    
    ### Rule curve parameters ###
    # Points defining the curves 
    # (linear interpolation will be applied to define the curves between the points)
    curve_dates = ['1 Apr',    '1 Aug',    '1 Dec',    '31 Mar']
    s_2_inc = 0.3 
    s_0         = [s_min/s_max,s_min/s_max,s_min/s_max,s_min/s_max]
    s_1         = [s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value] 
    s_2         = [s_1_0.value+s_2_inc,s_1_1.value+s_2_inc,s_1_2.value+s_2_inc,s_1_0.value+s_2_inc] 
    s_3         = [s_max/s_max,s_max/s_max,s_max/s_max,s_max/s_max]
    # Points defining the operating policy across the year 
    # (linear interpolation will be applied to define the curves between the points)
    rule_dates  = ['21 Mar',     '21 Jun',     '21 Sep',     '21 Dec']
    u_0         = [Qreg_rel_min, Qreg_rel_min, Qreg_rel_min, Qreg_rel_min]
    u_1         = [Qreg_rel_mean,Qreg_rel_mean,Qreg_rel_mean,Qreg_rel_mean]
    u_2         = [Qreg_rel_mean,Qreg_rel_mean,Qreg_rel_mean,Qreg_rel_mean]
    u_3         = [Qreg_rel_max, Qreg_rel_max, Qreg_rel_max, Qreg_rel_max]
    
    param = {'curves':{'year_date'    : curve_dates,
                       'storage_frac' : [s_0,s_1,s_2,s_3]},
             'rules' :{'year_date' : rule_dates,
                       'release'   : [u_0,u_1,u_2,u_3]}} # max release
    s_yday,r_yday = rule_curve(param)
    
    
    ### Figures ###
    # Fig 1a: Rule curve
    
    x_sc_1a = LinearScale(); y_sc_1a = LinearScale(min=0,max=1)
    x_ax_1a = Axis(label='day of the year', scale=x_sc_1a, grid_lines = 'none')
    y_ax_1a = Axis(label='storage fraction', scale=y_sc_1a, orientation='vertical', grid_lines = 'none')
    
    rule_curve_1 = Lines(x = np.arange(1,367), y = s_yday[1],
                         colors=['blue'], stroke = 'lightgray',
                         scales={'x': x_sc_1a, 'y': y_sc_1a},
                         fill   = 'top',fill_opacities = [1],fill_colors = ['blue'])
    rule_curve_2 = Lines(x = np.arange(1,367), y = s_yday[2],
                         colors=['blue'], stroke = 'lightgray',
                         scales={'x': x_sc_1a, 'y': y_sc_1a},
                         fill   = 'top',fill_opacities = [1],fill_colors = ['lightblue'])
    
    fig_1a             = plt.Figure(marks = [rule_curve_1,rule_curve_2],
                                   title = 'Rule curves',
                                   axes=[x_ax_1a, y_ax_1a],
                                   layout={'width': '500px', 'height': '250px'},
                                   background_style = {'fill': 'darkblue'},
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1a, 'y': y_sc_1a})
    
    rule_curve_1.observe(update_figure, ['x', 'y'])
    rule_curve_2.observe(update_figure, ['x', 'y'])
    
    ### Fig 2: Policy functions
    # Fig 2a: Policy function 1 Apr (year day = 91)
    x0 = [s_min/s_max,         Qreg_rel_min]
    x1 = [s_1_0.value,         Qreg_rel_mean]
    x2 = [s_1_0.value+s_2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,         Qreg_rel_max]
    param_a = x0, x1, x2, x3
    u_frac_a = policy_function(param_a)

    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step)
    x_sc_2 = LinearScale(min=0,max=1); y_sc_2 = LinearScale(min=0,max=Qreg_rel_max);
    x_ax_2 = Axis(label='Storage fraction', scale=x_sc_2); 
    y_ax_2 = Axis(label='Release (ML/week)', scale=y_sc_2, orientation='vertical')
    
    pol_func_a          = Lines(x      = s_frac,
                                y      = u_frac_a,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2a             = plt.Figure(marks = [pol_func_a],
                                   title = 'Policy function '+curve_dates[0],
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '400px', 'height': '300px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_a.observe(update_figure, ['x', 'y'])

    # Fig 2b: Policy function 1 Aug (year day = 213)
    x0 = [s_min/s_max,         Qreg_rel_min]
    x1 = [s_1_1.value,         Qreg_rel_mean]
    x2 = [s_1_1.value+s_2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,         Qreg_rel_max]
    param_b = x0, x1, x2, x3
    u_frac_b = policy_function(param_b)
    
    pol_func_b          = Lines(x      = s_frac,
                                y      = u_frac_b,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2b             = plt.Figure(marks = [pol_func_b],
                                   title = 'Policy function '+curve_dates[1],
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '400px', 'height': '300px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_b.observe(update_figure, ['x', 'y'])

    # Fig 2c: Policy function 1 Dec (year day = 335)
    x0 = [s_min/s_max,         Qreg_rel_min]
    x1 = [s_1_2.value,         Qreg_rel_mean]
    x2 = [s_1_2.value+s_2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,         Qreg_rel_max]
    param_c = x0, x1, x2, x3
    u_frac_c = policy_function(param_c)
    
    pol_func_c          = Lines(x      = s_frac,
                                y      = u_frac_c,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2c             = plt.Figure(marks = [pol_func_c],
                                   title = 'Policy function '+curve_dates[2],
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '400px', 'height': '300px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_c.observe(update_figure, ['x', 'y'])
    
    return fig_1a,fig_2a,fig_2b,fig_2c,s_1_0,s_1_1,s_1_2

def Interactive_rule_curve_manual(Res_sys_sim, policy_function, rule_curve,
                                  date, 
                                  I, e, 
                                  s_ini, s_min, s_max, 
                                  Qreg_rel_mean,Qreg_rel_min,Qreg_rel_max,
                                  cs, d):
    
    N = date.size # weeks
    #Function to update the rule curve when changing the parameters with the sliders
    def update_rule_curve(s_1_0,s_1_1,s_1_2,s_1_3): 

        s_1         = [s_1_0,s_1_1,s_1_2,s_1_3] 
        s_2         = [s_1_0+s_2_inc,s_1_1+s_2_inc,s_1_2+s_2_inc,s_1_3+s_2_inc]
        
        param = {'curves':{'year_date'    : curve_dates,
                           'storage_frac' : [s_0,s_1,s_2,s_3]},
        
                 'rules' :{'year_date' : rule_dates,
                           'release'   : [u_0,u_1,u_2,u_3]}} # max release
        s_yday,r_yday = rule_curve(param)
        
        x0 = [s_min/s_max,   Qreg_rel_min]
        x1 = [s_1_0,         Qreg_rel_mean]
        x2 = [s_1_0+s_2_inc, Qreg_rel_mean]
        x3 = [s_max/s_max,   Qreg_rel_max]
        param_a = x0, x1, x2, x3
        u_frac_a = policy_function(param_a)

        x0 = [s_min/s_max,   Qreg_rel_min]
        x1 = [s_1_1,         Qreg_rel_mean]
        x2 = [s_1_1+s_2_inc, Qreg_rel_mean]
        x3 = [s_max/s_max,   Qreg_rel_max]
        param_b = x0, x1, x2, x3
        u_frac_b = policy_function(param_b)
        
        x0 = [s_min/s_max,   Qreg_rel_min]
        x1 = [s_1_2,         Qreg_rel_mean]
        x2 = [s_1_2+s_2_inc, Qreg_rel_mean]
        x3 = [s_max/s_max,   Qreg_rel_max]
        param_c = x0, x1, x2, x3
#        print(param_c)
        u_frac_c = policy_function(param_c) 
        
        Qreg = {'releases' : {'type'  : 'rule curve',
                              'input' : [policy_function, rule_curve],
                              'param' : param},
                'inflows' : [],
                'rel_inf' : []}
        
        Qenv, Qspill, u, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, Qreg_rel_min, d, Qreg)
        
        TSD = (np.sum((np.maximum(d-u,np.zeros((N,1))))**2)).astype('int')
        fig_1b.title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2'
        
        CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
        fig_1c.title = 'Reservoir storage volume - MSV = '+str(CSV)+' ML'
    
        return s_yday[1],s_yday[2], u_frac_a, u_frac_b, u_frac_c, Qenv, Qspill, u, I_reg, s
    
    # Function to update the figures when changing the parameters with the sliders
    def update_figure(change):
        rule_curve_1.y = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[0]
        rule_curve_2.y = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[1]
        pol_func_a.y   = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[2]
        pol_func_b.y   = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[3]
        pol_func_c.y   = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[4]
        releases.y = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[7][:,0]
        storage.y = update_rule_curve(s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value)[9][:,0]
    
    # Definition of the sliders (Points defining the curves) 
    curve_dates = ['1 Apr',    '1 Aug',    '1 Dec',    '31 Mar']
    s_1_0 = widgets.FloatSlider(min=0, max=0.705, value=0.60, step=0.01, 
                                description = 's1 at '+str(curve_dates[0])+': ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s_1_0.observe(update_figure,names = 'value')
    
    s_1_1 = widgets.FloatSlider(min=0, max=0.705, value=0.30, step=0.01, 
                                description = 's1 at '+str(curve_dates[1])+': ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s_1_1.observe(update_figure,names = 'value')
    
    s_1_2 = widgets.FloatSlider(min=0, max=0.705, value=0.20, step=0.01, 
                                description = 's1 at '+str(curve_dates[2])+': ',
                                orientation='vertical',
                                layout={'width': '100px'},
                                continuous_update=False)
    s_1_2.observe(update_figure,names = 'value')
    
    
    # Initial simulation applying the default slider values of the parameters 
    # Points defining the curves
    s_2_inc = 0.3    
    s_0         = [s_min/s_max,s_min/s_max,s_min/s_max,s_min/s_max]
    s_1         = [s_1_0.value,s_1_1.value,s_1_2.value,s_1_0.value] 
    s_2         = [s_1_0.value+s_2_inc,s_1_1.value+s_2_inc,s_1_2.value+s_2_inc,s_1_0.value+s_2_inc] 
    s_3         = [s_max/s_max,s_max/s_max,s_max/s_max,s_max/s_max]
    # Points defining the operating policy across the year 
    rule_dates  = ['21 Mar',     '21 Jun',     '21 Sep',     '21 Dec']
    u_0         = [Qreg_rel_min, Qreg_rel_min, Qreg_rel_min, Qreg_rel_min]
    u_1         = [Qreg_rel_mean,Qreg_rel_mean,Qreg_rel_mean,Qreg_rel_mean]
    u_2         = [Qreg_rel_mean,Qreg_rel_mean,Qreg_rel_mean,Qreg_rel_mean]
    u_3         = [Qreg_rel_max, Qreg_rel_max, Qreg_rel_max, Qreg_rel_max]
    
    param = {'curves':{'year_date'    : curve_dates,
                       'storage_frac' : [s_0,s_1,s_2,s_3]},
    
             'rules' :{'year_date' : rule_dates,
                       'release'   : [u_0,u_1,u_2,u_3]}} # max release
    
    s_yday,r_yday = rule_curve(param)

    Qreg = {'releases' : {'type'  : 'rule curve',
                          'input' : [policy_function, rule_curve],
                          'param' : param},
            'inflows' : [],
            'rel_inf' : []}
    
    Qenv, Qspill, u, I_reg, s, E = Res_sys_sim(date, 
                                               I, e, 
                                               s_ini, s_min, s_max, 
                                               Qreg_rel_min, d, 
                                               Qreg)
    
    ### Figures ###
    # Fig 1a: Rule curve
    
    x_sc_1a = LinearScale(); y_sc_1a = LinearScale(min=0,max=1)
    x_ax_1a = Axis(label='day of the year', scale=x_sc_1a, grid_lines = 'none')
    y_ax_1a = Axis(label='storage fraction', scale=y_sc_1a, orientation='vertical', grid_lines = 'none')
    
    rule_curve_1 = Lines(x = np.arange(1,367), y = s_yday[1],
                         colors=['blue'], stroke = 'lightgray',
                         scales={'x': x_sc_1a, 'y': y_sc_1a},
                         fill   = 'top',fill_opacities = [1],fill_colors = ['blue'])
    rule_curve_2 = Lines(x = np.arange(1,367), y = s_yday[2],
                         colors=['blue'], stroke = 'lightgray',
                         scales={'x': x_sc_1a, 'y': y_sc_1a},
                         fill   = 'top',fill_opacities = [1],fill_colors = ['lightblue'])
    
    fig_1a             = plt.Figure(marks = [rule_curve_1,rule_curve_2],
                                   title = 'Rule curve',
                                   axes=[x_ax_1a, y_ax_1a],
                                   layout={'width': '500px', 'height': '250px'},
                                   background_style = {'fill': 'darkblue'},
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1a, 'y': y_sc_1a})
    
    rule_curve_1.observe(update_figure, ['x', 'y'])
    rule_curve_2.observe(update_figure, ['x', 'y'])
    
    # Fig 1b: Releases vs Demand
    x_sc_1b = DateScale();         y_sc_1b = LinearScale(min=0,max=Qreg_rel_max);
    x_ax_1b = Axis(scale=x_sc_1b); y_ax_1b = Axis(label='ML/week', scale=y_sc_1b, orientation='vertical')
    
    demand             = Bars(x      = date,
                              y      = d[:,0],
                              colors = ['gray'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b})
    
    releases           = Bars(x      = date,
                              y      = u[:,0],
                              colors = ['green'],
                              scales = {'x': x_sc_1b, 'y': y_sc_1b})
    
    TSD = (np.sum((np.maximum(d-u,np.zeros((N,1))))**2)).astype('int')
    
    fig_1b             = plt.Figure(marks = [demand, releases],
                                   title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                                   axes=[x_ax_1b, y_ax_1b],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1b, 'y': y_sc_1b})
    
    releases.observe(update_figure, ['x', 'y'])
    
    # Fig 1c: Storage
    x_sc_1c = DateScale(min=date[0]);                    y_sc_1c = LinearScale(min=0,max=200);
    x_ax_1c = Axis(scale=x_sc_1c); y_ax_1c = Axis(label='ML', scale=y_sc_1c, orientation='vertical')
    
    storage           = Lines(x      = date,
                              y      = s[:,0] ,
                              colors = ['blue'],
                              scales = {'x': x_sc_1c, 'y': y_sc_1c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x=date,
                                 y=[s_max]*(N+1),
                                 colors=['red'],
                                 scales={'x': x_sc_1c, 'y': y_sc_1c})
    
#    max_storage_label = plt.label(text = ['max storage'], 
#                                  x=['2015-01-01T00:00:00.000000000'],
#                                  y=[0],
#                                  colors=['red'])
    
    cri_storage = plt.plot(date,cs,
                             scales={'x': x_sc_1c, 'y': y_sc_1c},
                             colors=['red'],opacities = [1],
                             line_style = 'dashed',
                             fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)
#    cri_storage_label = plt.label(text = ['critical storage'], 
#                                    x=[0], # don't know what is the right format
#                                    y=[cs[0]-10],
#                                    colors=['red'])
    
    CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
    
    fig_1c             = plt.Figure(marks = [storage,max_storage,#max_storage_label,
                                            cri_storage],#,cri_storage_label],
                                   title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML',
                                   axes=[x_ax_1c, y_ax_1c],
                                   layout={'width': '950px', 'height': '150px'}, 
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_1c, 'y': y_sc_1c})
    
    storage.observe(update_figure, ['x', 'y'])
    
    ### Fig 2: Policy functions
    # Fig 2a: Policy function 1 Apr (year day = 91)
    x0 = [s_min/s_max,         Qreg_rel_min]
    x1 = [s_1_0.value,         Qreg_rel_mean]
    x2 = [s_1_0.value+s_2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,         Qreg_rel_max]
    param_a = x0, x1, x2, x3
    u_frac_a = policy_function(param_a)

    s_step = 0.01
    s_frac = np.arange(0,1+s_step,s_step)
    x_sc_2 = LinearScale(min=0,max=1); y_sc_2 = LinearScale(min=0,max=Qreg_rel_max);
    x_ax_2 = Axis(label='Storage fraction', scale=x_sc_2); 
    y_ax_2 = Axis(label='Release (ML/week)', scale=y_sc_2, orientation='vertical')
    
    pol_func_a          = Lines(x      = s_frac,
                                y      = u_frac_a,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2a             = plt.Figure(marks = [pol_func_a],
                                   title = 'Policy function '+curve_dates[0],
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '300px', 'height': '200px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_a.observe(update_figure, ['x', 'y'])

    # Fig 2b: Policy function 1 Aug (year day = 213)
    x0 = [s_min/s_max,         Qreg_rel_min]
    x1 = [s_1_1.value,         Qreg_rel_mean]
    x2 = [s_1_1.value+s_2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,         Qreg_rel_max]
    param_b = x0, x1, x2, x3
    u_frac_b = policy_function(param_b)
    
    pol_func_b          = Lines(x      = s_frac,
                                y      = u_frac_b,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2b             = plt.Figure(marks = [pol_func_b],
                                   title = 'Policy function '+curve_dates[1],
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '300px', 'height': '200px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_b.observe(update_figure, ['x', 'y'])

    # Fig 2c: Policy function 1 Dec (year day = 335)
    x0 = [s_min/s_max,         Qreg_rel_min]
    x1 = [s_1_2.value,         Qreg_rel_mean]
    x2 = [s_1_2.value+s_2_inc, Qreg_rel_mean]
    x3 = [s_max/s_max,         Qreg_rel_max]
    param_c = x0, x1, x2, x3
    u_frac_c = policy_function(param_c)
    
    pol_func_c          = Lines(x      = s_frac,
                                y      = u_frac_c,
                                colors = ['blue'],
                                scales = {'x': x_sc_2, 'y': y_sc_2})
    
    fig_2c             = plt.Figure(marks = [pol_func_c],
                                   title = 'Policy function '+curve_dates[2],
                                   axes = [x_ax_2, y_ax_2],
                                   layout = {'width': '300px', 'height': '200px'}, 
                                   animation_duration = 1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales = {'x': x_sc_2, 'y': y_sc_2})
    
    pol_func_c.observe(update_figure, ['x', 'y'])
    
    return fig_1a,fig_1b,fig_1c,fig_2a,fig_2b,fig_2c,s_1_0,s_1_1,s_1_2

def Interactive_rule_curve_auto(Res_sys_sim,policy_function,rule_curve,
                                date,
                                I,e, 
                                s_ini, s_min, s_max, 
                                u_mean, u_min, u_max,
                                cs, d,
                                results1_optim,results2_optim,sol_optim):
    
    N = date.size # weeks
    # Function to update the rule curve when clicking on the points of the Pareto front
    def update_rule_curve(i):
        
        s_1 = sol_optim[i]+[sol_optim[i][0]]
        s_2 = [s_1[0]+s_2_inc,s_1[1]+s_2_inc,s_1[2]+s_2_inc,s_1[0]+s_2_inc] 
        
        param = {'curves':{'year_date'    : curve_dates,
                           'storage_frac' : [s_0,s_1,s_2,s_3]},
        
                 'rules' :{'year_date' : rule_dates,
                           'release'   : [u_0,u_1,u_2,u_3]}} # max release
        s_yday,r_yday = rule_curve(param)
        
        s_yday,r_yday = rule_curve(param)
        
        Qreg = {'releases' : {'type'  : 'rule curve',
                              'input' : [policy_function, rule_curve],
                              'param' : param},
                'inflows' : [],
                'rel_inf' : []}
        
        Qenv, Qspill, u, I_reg, s, E = Res_sys_sim(date, I, e, s_ini, s_min, s_max, u_min, d, Qreg)
        
        TSD = (np.sum((np.maximum(d-u,np.zeros((N,1))))**2)).astype('int')
        fig_2b.title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2'
        
        CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
        fig_2c.title = 'Reservoir storage volume - MSV = '+str(CSV)+' ML'
        
        return s_yday[1],s_yday[2], Qenv, Qspill, u, I_reg, s
    
    # Function to update the figures when clicking on the points of the Pareto front
    def update_figure(change):
        if pareto_front.selected == None:
            pareto_front.selected = [0]        
        rule_curve_1.y = update_rule_curve(pareto_front.selected[0])[0]
        rule_curve_2.y = update_rule_curve(pareto_front.selected[0])[1]
        releases.y = update_rule_curve(pareto_front.selected[0])[4][:,0]
        storage.y = update_rule_curve(pareto_front.selected[0])[6][:,0]
    
    # Fig_pf: Pareto front  
    x_sc_pf = LinearScale();y_sc_pf = LinearScale()
    x_ax_pf = Axis(label='Total squared deficit [ML^2]', scale=x_sc_pf)
    y_ax_pf = Axis(label='Critical storage violation [ML]', scale=y_sc_pf, orientation='vertical')
    
    pareto_front = plt.scatter(results1_optim[:],results2_optim[:],
                               scales={'x': x_sc_pf, 'y': y_sc_pf},
                               colors=['deepskyblue'], 
                               interactions={'hover':'tooltip','click': 'select'})
    
    pareto_front.unselected_style={'opacity': 0.4}
    pareto_front.selected_style={'fill': 'red', 'stroke': 'yellow', 'width': '1125px', 'height': '125px'}
    def_tt = Tooltip(fields=['index','x', 'y'],
                     labels=['index','Water deficit', 'Critical storage'], 
                     formats=['.d','.1f', '.1f'])
    pareto_front.tooltip=def_tt
    
    fig_pf = plt.Figure(marks = [pareto_front],title = 'Pareto front', 
                        axes=[x_ax_pf, y_ax_pf],
                        layout={'width': '350px', 'height': '300px'}, 
                        animation_duration=1000,
                        fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0})
    
    if pareto_front.selected == []:
        pareto_front.selected = [0]
    
    pareto_front.observe(update_figure,'selected')
    
    # Initial simulation applting the point of the Pareto Fron selected by default  
    # Points defining the curves
    curve_dates = ['1 Apr',    '1 Aug',    '1 Dec',    '31 Mar']
    s_2_inc = 0.3    
    s_0         = [s_min/s_max,s_min/s_max,s_min/s_max,s_min/s_max]
    s_1         = sol_optim[pareto_front.selected[0]]+[sol_optim[pareto_front.selected[0]][0]]
    s_2         = [s_1[0]+s_2_inc,s_1[1]+s_2_inc,s_1[2]+s_2_inc,s_1[0]+s_2_inc] 
    s_3         = [s_max/s_max,s_max/s_max,s_max/s_max,s_max/s_max]
    # Points defining the operating policy across the year 
    rule_dates  = ['21 Mar',     '21 Jun',     '21 Sep',     '21 Dec']
    u_0         = [u_min, u_min, u_min, u_min]
    u_1         = [u_mean,u_mean,u_mean,u_mean]
    u_2         = [u_mean,u_mean,u_mean,u_mean]
    u_3         = [u_max, u_max, u_max, u_max]
    
    param = {'curves':{'year_date'    : curve_dates,
                       'storage_frac' : [s_0,s_1,s_2,s_3]},
    
             'rules' :{'year_date' : rule_dates,
                       'release'   : [u_0,u_1,u_2,u_3]}} # max release
    
    s_yday,r_yday = rule_curve(param)

    Qreg = {'releases' : {'type'  : 'rule curve',
                          'input' : [policy_function, rule_curve],
                          'param' : param},
            'inflows' : [],
            'rel_inf' : []}
    
    Qenv, Qspill, u, I_reg, s, E = Res_sys_sim(date, 
                                               I, e, 
                                               s_ini, s_min, s_max, 
                                               u_min, d, 
                                               Qreg)
    
    ### Figures ###
    # Fig 2a: Rule curve
    
    x_sc_2a = LinearScale(); y_sc_2a = LinearScale(min=0,max=1)
    x_ax_2a = Axis(label='day of the year', scale=x_sc_2a, grid_lines = 'none')
    y_ax_2a = Axis(label='storage fraction', scale=y_sc_2a, orientation='vertical', grid_lines = 'none')
    
    rule_curve_1 = Lines(x = np.arange(1,367), y = s_yday[1],
                         colors=['blue'], stroke = 'lightgray',
                         scales={'x': x_sc_2a, 'y': y_sc_2a},
                         fill   = 'top',fill_opacities = [1],fill_colors = ['blue'])
    rule_curve_2 = Lines(x = np.arange(1,367), y = s_yday[2],
                         colors=['blue'], stroke = 'lightgray',
                         scales={'x': x_sc_2a, 'y': y_sc_2a},
                         fill   = 'top',fill_opacities = [1],fill_colors = ['lightblue'])
    
    fig_2a             = plt.Figure(marks = [rule_curve_1,rule_curve_2],
                                   title = 'Rule curves',
                                   axes=[x_ax_2a, y_ax_2a],
                                   layout={'width': '500px', 'height': '300px'},
                                   background_style = {'fill': 'darkblue'},
                                   animation_duration=1000,
                                   fig_margin={'top':0, 'bottom':40, 'left':60, 'right':0},
                                   scales={'x': x_sc_2a, 'y': y_sc_2a})
    
    rule_curve_1.observe(update_figure, ['x', 'y'])
    rule_curve_2.observe(update_figure, ['x', 'y'])
    
    # Fig 2b: Releases vs Demand
    x_sc_2b = DateScale();         y_sc_2b = LinearScale(min=0,max=u_max);
    x_ax_2b = Axis(scale=x_sc_2b); y_ax_2b = Axis(label='ML/week', scale=y_sc_2b, orientation='vertical')
    
    demand             = Bars(x      = date,
                              y      = d[:,0],
                              colors = ['gray'],
                              scales = {'x': x_sc_2b, 'y': y_sc_2b})
    
    releases           = Bars(x      = date,
                              y      = u[:,0],
                              colors = ['green'],
                              scales = {'x': x_sc_2b, 'y': y_sc_2b})
    
    TSD = (np.sum((np.maximum(d-u,np.zeros((N,1))))**2)).astype('int')
    
    fig_2b = plt.Figure(marks = [demand, releases],
                        title = 'Supply vs Demand - TSD = '+str(TSD)+' ML^2',
                        axes = [x_ax_2b, y_ax_2b],
                        layout = {'width': '950px', 'height': '150px'}, 
                        animation_duration = 1000,
                        fig_margin = {'top':0, 'bottom':40, 'left':60, 'right':0},
                        scales = {'x': x_sc_2b, 'y': y_sc_2b})
    
    releases.observe(update_figure, ['x', 'y'])
    
    # Fig 2c: Storage
    x_sc_2c = DateScale();                    y_sc_2c = LinearScale(min=0,max=200);
    x_ax_2c = Axis(scale=x_sc_2c); y_ax_2c = Axis(label='ML', scale=y_sc_2c, orientation='vertical')
    
    storage           = Lines(x      = date,
                              y      = s[:,0],
                              colors = ['blue'],
                              scales = {'x': x_sc_2c, 'y': y_sc_2c},
                              fill   = 'bottom',fill_opacities = [0.8],fill_colors = ['blue'])
    
    max_storage       = plt.plot(x      = date,
                                 y      = [s_max]*(N+1),
                                 colors = ['red'],
                                 scales = {'x': x_sc_2c, 'y': y_sc_2c})
    
    # max_storage_label = plt.label(text = ['Max storage'], 
    #                               x=[0],
    #                               y=[s_max+15],
    #                               colors=['red'])
    
    cri_storage = plt.plot(date,cs,
                           scales={'x': x_sc_2c, 'y': y_sc_2c},
                           colors=['red'],opacities = [1],
                           line_style = 'dashed',
                           fill = 'bottom',fill_opacities = [0.4],fill_colors = ['red'], stroke_width = 1)
    # cri_storage_label = plt.label(text = ['Min storage'], 
    #                                 x=[0],
    #                                 y=[cs[0]-10],
    #                                 colors=['red'])
    
    CSV = (np.sum((np.maximum(cs-s,np.zeros((N+1,1)))))).astype('int')
    
    fig_2c = plt.Figure(marks = [storage,max_storage,cri_storage],
                        title = 'Reservoir storage volume - CSV = '+str(CSV)+' ML',
                        axes = [x_ax_2c, y_ax_2c],
                        layout = {'width': '950px', 'height': '150px'}, 
                        animation_duration = 1000,
                        fig_margin = {'top':0, 'bottom':40, 'left':60, 'right':0},
                        scales = {'x': x_sc_2c, 'y': y_sc_2c})
    
    storage.observe(update_figure, ['x', 'y'])
    
    return fig_pf, fig_2a,fig_2b,fig_2c