from pathlib import Path
import fitz

SRC = Path('/mnt/data/Figure03_POWDER_direction_and_cycle_variation_v2(1).pdf')
OUT = Path('/mnt/data/WellPulse_FigureCaption_Upgrade_R14_RF9H_2026-08-30/upgrade/figures/Figure03_POWDER_direction_and_cycle_variation_v2_LOSS_CORRECTED.pdf')
REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'

doc = fitz.open(SRC)
p = doc[0]
# Remove only Panel C's old plot, y-axis label, and title from the original vector page.
for r in [
    fitz.Rect(45.8,188.4,245.8,311.2),   # plot interior + spines
    fitz.Rect(7.0,202.0,24.8,299.0),     # y label only
    fitz.Rect(44.0,170.0,245.0,187.5),   # title only
]:
    p.add_redact_annot(r, fill=(1,1,1))
p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED, text=fitz.PDF_REDACT_TEXT_REMOVE)

p.insert_font(fontname='LiberationSans', fontfile=REG)
p.insert_font(fontname='LiberationSans-Bold', fontfile=BOLD)

x_axis = [58.095340728759766, 116.5880355834961, 175.0807342529297, 233.5734405517578]
y0 = 308.4683837890625
y100 = 192.48760986328125
scale = (y0-y100)/100.0
def y(v): return y0-v*scale

# axes and ticks
p.draw_line(fitz.Point(46.39680099487305,310.78802490234375),fitz.Point(46.39680099487305,189.0081787109375),color=(0,0,0),width=0.8,overlay=True)
p.draw_line(fitz.Point(46.39680099487305,310.78802490234375),fitz.Point(245.27197265625,310.78802490234375),color=(0,0,0),width=0.8,overlay=True)
for x in x_axis:
    p.draw_line(fitz.Point(x,310.78802490234375),fitz.Point(x,314.28802490234375),color=(0,0,0),width=0.8,overlay=True)
for v in [0,20,40,60,80,100]:
    yy=y(v); p.draw_line(fitz.Point(46.39680099487305,yy),fitz.Point(42.89680099487305,yy),color=(0,0,0),width=0.8,overlay=True)

# helper: dashed segments built explicitly, avoiding backend-dependent PDF dash operators
def patterned_segment(a,b,pattern):
    dx=b.x-a.x; dy=b.y-a.y; L=(dx*dx+dy*dy)**0.5
    if L==0: return
    ux,uy=dx/L,dy/L
    pos=0.0; draw=True; i=0
    while pos<L:
        seg=pattern[i%len(pattern)]; nxt=min(L,pos+seg)
        if draw:
            p.draw_line(fitz.Point(a.x+ux*pos,a.y+uy*pos),fitz.Point(a.x+ux*nxt,a.y+uy*nxt),color=(0,0,0),width=1.0,overlay=True)
        pos=nxt; draw=not draw; i+=1

def polyline(points,style):
    for a,b in zip(points[:-1],points[1:]):
        if style=='solid': p.draw_line(a,b,color=(0,0,0),width=1.0,overlay=True)
        elif style=='dash': patterned_segment(a,b,[3.7,1.6])
        else: patterned_segment(a,b,[1.0,1.65])

def marker(pt,kind):
    r=2.75
    if kind=='circle':
        p.draw_circle(pt,r,color=(0,0,0),fill=(1,1,1),width=1.0,overlay=True)
    elif kind=='square':
        p.draw_rect(fitz.Rect(pt.x-r,pt.y-r,pt.x+r,pt.y+r),color=(0,0,0),fill=(0.65,0.65,0.65),width=1.0,overlay=True)
    else:
        sh=p.new_shape(); sh.draw_polyline([fitz.Point(pt.x,pt.y-r),fitz.Point(pt.x-r,pt.y+r),fitz.Point(pt.x+r,pt.y+r),fitz.Point(pt.x,pt.y-r)])
        sh.finish(color=(0,0,0),fill=(0,0,0),width=1.0); sh.commit(overlay=True)

# Frozen measured E3 loss values.
series=[
    ([0,5,10,80],'solid','circle'),
    ([0,0,5,65],'dash','square'),
    ([0,5,50,70],'dot','triangle'),
]
for vals,style,mk in series:
    pts=[fitz.Point(x,y(v)) for x,v in zip(x_axis,vals)]
    polyline(pts,style)
    for pt in pts: marker(pt,mk)

# Legend matched to supplied v2 grammar: circle / gray square / black triangle + line style redundancy.
legend_y=207.0
centers=[59.7168,108.58555,157.45430]
styles=['solid','dash','dot']; mks=['circle','square','triangle']; labels=['cycle 1','cycle 2','cycle 3']
for c,st,mk in zip(centers,styles,mks):
    a=fitz.Point(c-6.66,legend_y); b=fitz.Point(c+6.66,legend_y)
    polyline([a,b],st); marker(fitz.Point(c,legend_y),mk)
# Place labels to the right of each marker, compactly, as in original.
for c,label in zip(centers,labels):
    p.insert_text(fitz.Point(c+8.5,209.9),label,fontname='LiberationSans',fontsize=5.5,color=(0,0,0),overlay=True)

# New title and y label only.
p.insert_text(fitz.Point(46.3968,181.8),'C  E3 repeated-cycle ICMP loss',fontname='LiberationSans-Bold',fontsize=8.5,color=(0,0,0),overlay=True)
p.insert_textbox(fitz.Rect(8.6,202.0,23.0,299.0),'ICMP loss (%)',fontname='LiberationSans',fontsize=7.5,color=(0,0,0),rotate=90,align=1,overlay=True)

meta=doc.metadata
meta.update({'title':'Figure 3 - POWDER direction dependence and repeated-cycle outcomes','author':'','subject':'Scientific figure candidate; Panel C corrected to frozen E3 ICMP loss semantics','creator':'Deterministic surgical vector patch of supplied v2 candidate'})
doc.set_metadata(meta)
doc.save(OUT,garbage=4,deflate=True,clean=True)
doc.close()
print(OUT)
