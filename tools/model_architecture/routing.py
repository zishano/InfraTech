"""Obstacle-aware orthogonal connection simplification for native diagrams.

Preserves all source/target pairs. Prefers a single segment, then a one-bend
path; existing routes remain when either simpler alternative hits a node.
"""

def simplify_connections(graph,clearance=6):
    nodes={n['id']:n for n in graph['nodes']}
    operations={k:n for k,n in nodes.items() if n.get('kind')!='decoration'}
    def rect(n):
        x,y,w,h=n['box'];return x,y,x+w,y+h
    def center(n):
        x,y,w,h=n['box'];return x+w/2,y+h/2
    def ellipse(n):return 'shape=ellipse' in n.get('style','')
    def hit(a,b,box,margin):
        x,y,xx,yy=box;x-=margin;y-=margin;xx+=margin;yy+=margin
        if abs(a[0]-b[0])<.001:
            return x+.01<a[0]<xx-.01 and min(max(a[1],b[1]),yy)-max(min(a[1],b[1]),y)>.01
        if abs(a[1]-b[1])<.001:
            return y+.01<a[1]<yy-.01 and min(max(a[0],b[0]),xx)-max(min(a[0],b[0]),x)>.01
        return True
    def clear(points,source,target):
        for k,n in operations.items():
            margin=0 if k in [source,target] else clearance
            for a,b in zip(points,points[1:]):
                if hit(a,b,rect(n),margin):return False
        return True
    def anchor(n,port):
        x,y,w,h=n['box'];return (round(x+w*port[0],4),round(y+h*port[1],4))
    def normal(port,delta,outward=True):
        dx,dy=delta
        if not outward:dx=-dx;dy=-dy
        return ((port[0]==0 and dx<0 and abs(dy)<.001) or
                (port[0]==1 and dx>0 and abs(dy)<.001) or
                (port[1]==0 and dy<0 and abs(dx)<.001) or
                (port[1]==1 and dy>0 and abs(dx)<.001))
    counts=dict(straight=0,one_bend=0,kept=0)
    for edge in graph['edges']:
        source,target=edge['source'],edge['target'];a,b=nodes[source],nodes[target]
        ax,ay,axx,ayy=rect(a);bx,by,bxx,byy=rect(b);acx,acy=center(a);bcx,bcy=center(b)
        candidates=[]
        # Exact common x/y ports remove even tiny automatic-router jogs.
        lo,hi=max(ax,bx),min(axx,bxx)
        if hi-lo>4 and (ayy<=by or byy<=ay):
            preferred=bcx if b['box'][2]<=a['box'][2] else acx
            options=[max(lo+1,min(hi-1,preferred)),(lo+hi)/2,lo+min(8,(hi-lo)/4),hi-min(8,(hi-lo)/4)]
            for x in options:
                if (not ellipse(a) or abs(x-acx)<.01) and (not ellipse(b) or abs(x-bcx)<.01):
                    ap=((x-ax)/(axx-ax),0 if bcy<acy else 1);bp=((x-bx)/(bxx-bx),1 if bcy<acy else 0)
                    pts=[anchor(a,ap),anchor(b,bp)]
                    if clear(pts,source,target):
                        candidates.append((0,abs(pts[0][1]-pts[1][1]),ap,bp,pts));break
        lo,hi=max(ay,by),min(ayy,byy)
        if hi-lo>4 and (axx<=bx or bxx<=ax):
            y=bcy if b['box'][3]<=a['box'][3] else acy
            y=max(lo+1,min(hi-1,y))
            if (not ellipse(a) or abs(y-acy)<.01) and (not ellipse(b) or abs(y-bcy)<.01):
                ap=(1 if bcx>acx else 0,(y-ay)/(ayy-ay));bp=(0 if bcx>acx else 1,(y-by)/(byy-by))
                pts=[anchor(a,ap),anchor(b,bp)]
                if clear(pts,source,target):candidates.append((0,abs(pts[0][0]-pts[1][0]),ap,bp,pts))
        if not candidates:
            ports=[(.5,0),(.5,1),(0,.5),(1,.5)]
            for ap in ports:
                start=anchor(a,ap)
                for bp in ports:
                    end=anchor(b,bp)
                    for corner in [(start[0],end[1]),(end[0],start[1])]:
                        if corner==start or corner==end:continue
                        if not normal(ap,(corner[0]-start[0],corner[1]-start[1])):continue
                        if not normal(bp,(end[0]-corner[0],end[1]-corner[1]),False):continue
                        pts=[start,corner,end]
                        if clear(pts,source,target):
                            length=abs(start[0]-end[0])+abs(start[1]-end[1])
                            candidates.append((1,length,ap,bp,pts))
        if candidates:
            bends,length,ap,bp,points=min(candidates,key=lambda t:t[:2])
            edge['ports']=[*ap,*bp];edge['routing']='straight'
            edge.pop('points',None)
            if bends:edge['points']=[list(points[1])]
            counts['one_bend' if bends else 'straight']+=1
        elif edge.get('routing')=='straight' and len(edge.get('points',[]))<=1:
            counts['one_bend' if edge.get('points') else 'straight']+=1
        else:counts['kept']+=1
    graph['routing_summary']=counts
    return graph
