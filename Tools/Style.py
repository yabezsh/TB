"""
Author: Federica Lionetto
Date: November 16th, 2015

Description:
Define some useful functions to be used to accomplish common tasks with ROOT objects.
- LHCbStyle()
- InitCanvas(canvas,top,bottom,left,right)
- InitHist(hist,title,x,y)
- InitHist2(hist,title,x,y,z)
- InitGraph(graph,title,x,y)
- SetStyleObj(obj,markerColor,lineColor,fillColor,fillStyle,markerSize,markerStyle,lineWidth,lineStyle)
- AdjustOffsets(hist,axis,labelOffset,titleOffset)
- DrawObj(canvas,obj,leg,option,folder)
- DrawOjbCompare(canvas,objList,optionDict,leg,folder)
- CreateLegend(objList,labelDict,optionDict,x1,y1,x2,y2)
- CreateStats(hist,option,x1,y1,x2,y2)
- TestStyle()

How to run it:
Include it in the other python scripts.
"""

from array import array

import numpy as np

import ROOT

def ColorList(n) :
    default_list = [ROOT.kViolet,
            ROOT.kTeal-5,
            ROOT.kRed,
            ROOT.kViolet+2,
            ROOT.kAzure+1,
            ROOT.kAzure-4,
            ROOT.kOrange,
            ROOT.kPink+9,
            ROOT.kOrange+8,
            ROOT.kGreen]
    result = []
    if (n <= len(default_list)) :
        result = default_list[:n] 
    else :
        mod = n%len(default_list)
        div = n/len(default_list)
        for i in range(div) :
            result = result + default_list
        result = result + default_list[:mod]
    print result
    return result

def LineStyleList(n) :
    default_list = [1,
                    2,
                    3,
                    4,
                    5]
    result = []
    for i in range(n) :
        result.append(default_list[(i/10)%5])
    print result
    return result

def LHCbStyle() :
    '''
    black = 1
    red = 2
    green = 3
    blue = 4
    yellow = 5
    magenta = 6
    cyan = 7
    purple = 9
    '''

    lhcbFont = 132
    lhcbWidth = 2
    lhcbTSize = 0.06

    # Fine.
    ROOT.gROOT.SetStyle('Plain')
    lhcbStyle = ROOT.TStyle('lhcbStyle','LHCb plots style')

    # Fine.
    lhcbStyle.SetFillColor(0)
    lhcbStyle.SetFillStyle(1001)
    lhcbStyle.SetFrameFillColor(0)
    lhcbStyle.SetFrameBorderMode(0)
    lhcbStyle.SetPadBorderMode(0)
    lhcbStyle.SetPadColor(0)
    lhcbStyle.SetCanvasBorderMode(0)
    lhcbStyle.SetCanvasColor(0)
    lhcbStyle.SetStatColor(0)
    lhcbStyle.SetLegendBorderSize(0)
    lhcbStyle.SetLegendFont(132)

    # Fine.
    # If you want the usual gradient palette (blue -> red)
    lhcbStyle.SetPalette(1)
    # If you want colors that correspond to gray scale in black and white
    # colors=array('i',[0,5,7,3,6,2,4,1])
    # lhcbStyle.SetPalette(len(colors),colors)

    # Fine.
    lhcbStyle.SetPaperSize(20,26)
    lhcbStyle.SetPadTopMargin(0.05)
    lhcbStyle.SetPadRightMargin(0.05)
    lhcbStyle.SetPadBottomMargin(0.16)
    lhcbStyle.SetPadLeftMargin(0.14)
    
    # Fine.
    lhcbStyle.SetTextFont(lhcbFont)
    lhcbStyle.SetTextSize(lhcbTSize)
    lhcbStyle.SetLabelFont(lhcbFont,"x")
    lhcbStyle.SetLabelFont(lhcbFont,"y")
    lhcbStyle.SetLabelFont(lhcbFont,"z")
    lhcbStyle.SetLabelSize(lhcbTSize,"x")
    lhcbStyle.SetLabelSize(lhcbTSize,"y")
    lhcbStyle.SetLabelSize(lhcbTSize,"z")
    lhcbStyle.SetTitleFont(lhcbFont)
    lhcbStyle.SetTitleFont(lhcbFont,"x")
    lhcbStyle.SetTitleFont(lhcbFont,"y")
    lhcbStyle.SetTitleFont(lhcbFont,"z")
    lhcbStyle.SetTitleSize(1.2*lhcbTSize,"x")
    lhcbStyle.SetTitleSize(1.2*lhcbTSize,"y")
    lhcbStyle.SetTitleSize(1.2*lhcbTSize,"z")

    # Fine.
    lhcbStyle.SetLineWidth(lhcbWidth)
    lhcbStyle.SetFrameLineWidth(lhcbWidth)
    lhcbStyle.SetHistLineWidth(lhcbWidth)
    lhcbStyle.SetFuncWidth(lhcbWidth)
    lhcbStyle.SetGridWidth(lhcbWidth)
    lhcbStyle.SetLineStyleString(2,"[12 12]")
    lhcbStyle.SetMarkerStyle(20)
    lhcbStyle.SetMarkerSize(1.0)

    # Fine.
    lhcbStyle.SetLabelOffset(0.010,"X")
    lhcbStyle.SetLabelOffset(0.010,"Y")

    # Fine.
    lhcbStyle.SetOptStat(0)
    lhcbStyle.SetStatFormat("6.3g")
    lhcbStyle.SetOptTitle(0)
    lhcbStyle.SetOptFit(0)
    lhcbStyle.SetTitleOffset(0.95,"X")
    lhcbStyle.SetTitleOffset(0.95,"Y")
    lhcbStyle.SetTitleOffset(1.2,"Z")
    lhcbStyle.SetTitleFillColor(0)
    lhcbStyle.SetTitleStyle(0)
    lhcbStyle.SetTitleBorderSize(0)
    lhcbStyle.SetTitleFont(lhcbFont,"title")
    lhcbStyle.SetTitleX(0.0)
    lhcbStyle.SetTitleY(1.0)
    lhcbStyle.SetTitleW(1.0)
    lhcbStyle.SetTitleH(0.05)

    # Fine.
    lhcbStyle.SetStatBorderSize(0)
    lhcbStyle.SetStatFont(lhcbFont)
    lhcbStyle.SetStatFontSize(0.05)
    lhcbStyle.SetStatX(0.9)
    lhcbStyle.SetStatY(0.9)
    lhcbStyle.SetStatW(0.25)
    lhcbStyle.SetStatH(0.15)
    
    # Fine.
    lhcbStyle.SetPadTickX(1)
    lhcbStyle.SetPadTickY(1)

    # Fine.
    lhcbStyle.SetNdivisions(505,"x")
    lhcbStyle.SetNdivisions(510,"y")

    # Fine.
    lhcbStyle.SetPaintTextFormat("5.2f")

    # Fine.
    ROOT.gROOT.SetStyle("lhcbStyle")
    # ROOT.gStyle = ROOT.gROOT.GetGlobal('gStyle',1)
    ROOT.gROOT.ForceStyle()

    # Fine.
    lhcbName = ROOT.TPaveText(ROOT.gStyle.GetPadLeftMargin() + 0.05,0.87 - ROOT.gStyle.GetPadTopMargin(),ROOT.gStyle.GetPadLeftMargin() + 0.20,0.95 - ROOT.gStyle.GetPadTopMargin(),'BRNDC')
    lhcbName.AddText("LHCb")
    lhcbName.SetFillColor(0)
    lhcbName.SetTextAlign(12)
    lhcbName.SetBorderSize(0)

    # Fine.
    lhcbLabel = ROOT.TText()
    lhcbLabel.SetTextFont(lhcbFont)
    lhcbLabel.SetTextColor(1)
    lhcbLabel.SetTextSize(lhcbTSize)
    lhcbLabel.SetTextAlign(12)

    # Fine.
    lhcbLatex = ROOT.TLatex()
    lhcbLatex.SetTextFont(lhcbFont)
    lhcbLatex.SetTextColor(1)
    lhcbLatex.SetTextSize(lhcbTSize)
    lhcbLatex.SetTextAlign(12)

    print '-------------------------'
    print 'Set LHCb Style - Feb 2012'
    print '-------------------------'

    return lhcbStyle

def InitCanvas(canvas,top=0.15,bottom=None,left=None,right=None) :
    """
    Initialise canvas <canvas> with top margin <top>, bottom margin <bottom>, left margin <left> and right margin <right>.
    """
    if top is not None :
        canvas.SetTopMargin(top)
    if bottom is not None :
        canvas.SetBottomMargin(bottom)
    if left is not None :
        canvas.SetLeftMargin(left)
    # Set the right margin to 0.19 for COLZ plots.
    if right is not None :
        canvas.SetRightMargin(right)
    return

def InitHist(hist,title='',x='',y='') :
    """
    Initialise 1D histogram <hist> with title <title>, x axis title <x>, and y axis title <y>.
    If <y> is not given, a y axis title based on the number of entries per bin is set.
    """
    hist.SetTitle(title)
    hist.GetXaxis().SetTitle(x)
    if (y=='') :
        hist.GetYaxis().SetTitle('Entries / {0}'.format(round(hist.GetBinWidth(1),2)))
    else :
        hist.GetYaxis().SetTitle(y)
    return

def InitHist2(hist,title='',x='',y='',z='') :
    """
    Initialise 2D histogram <hist> with title <title>, x axis title <x>, y axis title <y>, and z axis title <z>.
    If <z> is not given, a z axis title based on the number of entries per bin is set.
    """
    hist.SetTitle(title)
    hist.GetXaxis().SetTitle(x)
    hist.GetYaxis().SetTitle(y)
    if (z=='') :
        hist.GetZaxis().SetTitle('Entries / ({0}*{1})'.format(round(hist.GetXaxis().GetBinWidth(1),2),round(hist.GetYaxis().GetBinWidth(1),2)))
    else :
        hist.GetZaxis().SetTitle(z)
    return

def InitGraph(graph,title='',x='',y='') :
    """
    Initialise graph <graph> with title <title>, x axis title <x>, and y axis title <y>.
    """
    graph.SetTitle(title)
    graph.GetXaxis().SetTitle(x)
    graph.GetYaxis().SetTitle(y)
    return

def SetStyleObj(obj,markerColor=ROOT.kBlack,lineColor=ROOT.kMagenta,fillColor=None,fillStyle=1001,markerSize=1,markerStyle=20,lineWidth=2,lineStyle=1) :
    """
    Set the style of object <obj>:
    - marker color
    - line color
    - fill color
    - marker size
    - marker style
    - line width
    - line style
    A default value exists for the last four.
    """
    obj.SetMarkerColor(markerColor)
    obj.SetLineColor(lineColor)
    obj.SetFillStyle(fillStyle)
    if fillColor is not None :
        obj.SetFillColor(fillColor)
    obj.SetMarkerSize(markerSize)
    obj.SetMarkerStyle(markerStyle)
    obj.SetLineWidth(lineWidth)
    obj.SetLineStyle(lineStyle)
    return

def AdjustOffsets(hist,axis,labelOffset=0.005,titleOffset=0.85) :
    """
    Adjust the offsets of histogram <hist> along the axis <axis>, by setting the label offset <labelOffset> and the title offset <titleOffset>.
    The argument <axis> can be 'X', 'Y', or 'Z'.
    The default values are those used for a TH2 object one wants to draw with the COLZ option.
    """
    hist.SetLabelOffset(labelOffset,axis)
    hist.SetTitleOffset(titleOffset,axis)
    return

def DrawObj(canvas,obj,leg=None,option='',folder='./') :
    """
    Draw object <obj> in canvas <canvas>, together with legend <leg> (if provided), with option <option> and save the result in a pdf file having the same name as the canvas, located in the folder <folder>.
    """
    name=canvas.GetName()
    canvas.cd()
    obj.Draw(option)
    if ('A' in option) :
        canvas.SetTickx(1)
        canvas.SetTicky(1)
    if (leg is not None) :
        leg.Draw()
    canvas.Update()
    canvas.Write()
    canvas.Print(folder+name+'.pdf')
    canvas.Close()
    return

def DrawObjCompare(canvas,objList,optionDict,leg,folder='./') :
    """
    Draw list of objects <objList> in canvas <canvas>, together with legend <leg>, with option <optionDict> and save the result in a pdf file having the same name as the canvas, located in the folder <folder>.
    This allows to draw histograms, graphs, and functions in the same canvas.
    However, since graphs do not have a 'GetMaximum()' method, the object to be drawn first is searched for among histograms and functions only (whose names start with 'h' and 'f', respectively). The remaining objects are drawn after.
    """
    # print 'DrawObjCompare, optionDict: ', optionDict
    
    name=canvas.GetName()
    canvas.cd()
    
    containsTMultiGraph = False

    maxList = []
    for obj in objList :
        if (isinstance(obj,ROOT.TH1F) or isinstance(obj,ROOT.TF1)) :
            maxList.append(obj.GetMaximum())
        if (isinstance(obj,ROOT.TMultiGraph)) :
            containsTMultiGraph = True

    # print 'DrawObjCompare, maxList: ', maxList

    # print 'DrawObjCompare, containsTMultiGraph: ', containsTMultiGraph

    if containsTMultiGraph :
        for obj in objList :
            if (isinstance(obj,ROOT.TMultiGraph)) :
                obj.Draw(optionDict[obj.GetName()])
        
    if (len(maxList) != 0):
        firstDraw = int(maxList.index(max(maxList)))
        # print 'DrawObjCompare, firstDraw: ', firstDraw

        objList[firstDraw].Draw(optionDict[objList[firstDraw].GetName()])
        # print 'DrawObjCompare, objList: ', objList
        for obj in objList :
            if (obj != objList[firstDraw] and not isinstance(obj,ROOT.TMultiGraph)) :
                obj.Draw(optionDict[obj.GetName()]+'SAME')
                # print 'DrawObjCompare, obj: ', obj
    
    # print 'DrawObjCompare, optionDict: ', optionDict

    if leg is not None :
        leg.Draw()
    canvas.Update()
    canvas.Write()
    canvas.SaveAs(folder+name+'.pdf')
    canvas.Close()
    return

def CreateLegend(objList,labelDict,optionDict,x1=0.64,y1=0.59,x2=0.94,y2=0.89) :
    """
    Create legend <leg> starting from list of objects <objList>, dictionary of labels <labelDict>, and dictionary of options <optionDict>.
    The legend is displayed in the position identified by <x1>, <y1>, <x2>, and <y2>.
    If the option 'w' is specified, the fill color is set to white.
    The text size is set to '0.05'.
    """
    leg = ROOT.TLegend(x1,y1,x2,y2)
    leg.SetFillColor(ROOT.kWhite)
    for obj in objList :
        label = labelDict[obj.GetName()]
        option = optionDict[obj.GetName()]
        leg.AddEntry(obj,label,option)
    leg.SetTextSize(0.05)
    return leg

def CreateStats(hist,option,x1=0.64,y1=0.59,x2=0.94,y2=0.89) :
    """
    Create stats <stats> of histogram <hist> depending on option <option>.
    The stats are displayed in the position identified by <x1>, <y1>, <x2>, and <y2>.
    """
    stats = ROOT.TPaveStats(x1,y1,x2,y2,'brNDC')
    stats.SetName('stats')
    stats.SetBorderSize(1)
    stats.SetFillColor(0)
    stats.SetTextAlign(12)
    text = stats.AddText('Entries = {0}'.format(hist.GetEntries()))
    if ('I' in option) :
        text = stats.AddText('Integral = {0}'.format(hist.Integral()))
    N = hist.GetDimension()
    if (N == 1) :
        text = stats.AddText('Mean  = {0}'.format(hist.GetMean()));
        text = stats.AddText('RMS   = {0}'.format(hist.GetRMS()));
        if ('S' in option) :
            text = stats.AddText('Skewness = {0}'.format(hist.GetSkewness()))
        if ('K' in option) :
            text = stats.AddText('Kurtosis = {0}'.format(hist.GetKurtosis()))
        if ('U' in option) :
            text = stats.AddText('Underflow = {0}'.format(hist.GetBinContent(0)))
        if ('O' in option) :
            over = hist.GetNbinsX()+1
            text = stats.AddText('Overflow  = {0}'.format(hist.GetBinContent(over)))
    else :
        text = stats.AddText('Mean x = {0}'.format(hist.GetMean(1)))
        text = stats.AddText('Mean y = {0}'.format(hist.GetMean(2)))
        text = stats.AddText('RMS x  = {0}'.format(hist.GetRMS(1)))
        text = stats.AddText('RMS y  = {0}'.format(hist.GetRMS(2)))
        if ('S' in option) :
            text = stats.AddText('Skewness x = {0}'.format(hist.GetSkewness(1)))
            text = stats.AddText('Skewness y = {0}'.format(hist.GetSkewness(2)))
        if ('K' in option) :
            text = stats.AddText('Kurtosis x = {0}'.format(hist.GetKurtosis(1)))
            text = stats.AddText('Kurtosis y = {0}'.format(hist.GetKurtosis(2)))
        if ('U' in option or 'O' in option) :
            nbinsX = hist.GetNbinsX()
            nbinsY = hist.GetNbinsY()
            bl = hist.GetBinContent(0,0)
            bc = 0
            for i in range(1,nbinsX+1) :
                bc += hist.GetBinContent(i,0)
            br = hist.GetBinContent(nbinsX+1,0)
            cl = 0
            for i in range(1,nbinsY+1) :
                cl += hist.GetBinContent(0,i)
            cc = hist.GetEffectiveEntries()
            cr = 0
            for i in range(1,nbinsX+1) :
                cr += hist.GetBinContent(nbinsX+1,i)
            tl = hist.GetBinContent(0,nbinsY+1)
            tc = 0
            for i in range(1,nbinsX+1) :
                tc += hist.GetBinContent(i,nbinsY+1)
            tr = hist.GetBinContent(nbinsX+1,nbinsY+1)
            text = stats.AddText('{0}| {1}| {2}'.format(tl,tc,tr))
            text = stats.AddText('{0}| {1}| {2}'.format(cl,cc,cr))
            text = stats.AddText('{0}| {1}| {2}'.format(bl,bc,br))
    return stats

def TestStyle() :
    """
    Test the functions defined above in a quick and automatic way.
    """
    lhcbStyle = LHCbStyle()

    canvasDrawObj = ROOT.TCanvas('canvasDrawObj','canvasDrawObj',400,300)
    canvasDrawObjCompare = ROOT.TCanvas('canvasDrawObjCompare','canvasDrawObjCompare',400,300)
    canvasDrawObjCompare2 = ROOT.TCanvas('canvasDrawObjCompare2','canvasDrawObjCompare2',400,300)

    hist1 = ROOT.TH1F('hist1','hist1',100,0,10)
    hist2 = ROOT.TH1F('hist2','hist2',100,0,10)
    hist3 = ROOT.TH1F('hist3','hist3',100,0,10)

    hist2D = ROOT.TH2F('hist2D','hist2D',100,0,10,10,0,2)

    hist1.Fill(2,10)
    hist2.Fill(3,2)
    hist3.Fill(5,1)

    hist2D.Fill(2,1)
    hist2D.Fill(4,0)
    hist2D.Fill(5,2,10)

    ax = np.arange(0.,10.,2.)
    ay = ax*5.
    asize = len(ax)
    print ax
    print ay
    print asize
    graph = ROOT.TGraph(asize,ax,ay)
    graph.SetName('graph')

    # Test InitHist.
    InitHist(hist1,title='title for hist 1',x='x axis',y='y axis')
    InitHist(hist2,title='title for hist 2',x='x axis')
    InitHist(hist3,title='')

    # Test InitHist2.
    InitHist2(hist2D)

    # Test InitGraph.
    InitGraph(graph)

    markerColor=ROOT.kMagenta
    lineColor=ROOT.kMagenta
    fillColor=ROOT.kMagenta
    # Test SetStyleObj.
    SetStyleObj(hist1,markerColor,lineColor,fillColor)
    SetStyleObj(graph,markerColor,lineColor,fillColor)

    # Test AdjustOffsets.
    AdjustOffsets(hist2D,'Z')

    objList=[hist1,hist2,hist3]
    colorDict={hist1.GetName():ROOT.kRed,hist2.GetName():ROOT.kBlue,hist3.GetName():ROOT.kGreen}
    optionDrawDict={hist1.GetName():'E',hist2.GetName():'',hist3.GetName():'E'}
    labelDict={hist1.GetName():'first',hist2.GetName():'second',hist3.GetName():'third'}
    optionLegDict={hist1.GetName():'l',hist2.GetName():'p',hist3.GetName():'fw'}

    objList2=[hist1,graph]
    colorDict2={hist1.GetName():ROOT.kRed,graph.GetName():ROOT.kBlue}
    optionDrawDict2={hist1.GetName():'E',graph.GetName():'APC'}
    labelDict2={hist1.GetName():'first',graph.GetName():'second'}
    optionLegDict2={hist1.GetName():'l',graph.GetName():'pw'}

    print objList2
    print colorDict2
    print optionDrawDict2
    print labelDict2
    print optionLegDict2

    # Test DrawObj.
    DrawObj(canvasDrawObj,hist1)

    # Test CreateLegend.
    leg = CreateLegend(objList,labelDict,optionLegDict,0.5,0.5,0.8,0.7)
    leg2 = CreateLegend(objList2,labelDict2,optionLegDict2,0.6,0.2,0.9,0.5)

    # Test DrawObjCompare.
    DrawObjCompare(canvasDrawObjCompare,objList,colorDict,optionDrawDict,leg)
    DrawObjCompare(canvasDrawObjCompare2,objList2,colorDict2,optionDrawDict2,leg2)

    option = 'IUO'
    # Test CreateStats.
    CreateStats(hist1,option)

    return

LHCbStyle()
