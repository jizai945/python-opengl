from typing import Dict, List, Optional, Tuple, Set, Union
import copy
import traceback

class Point(object):
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        
    def x(self):
        return self._x

    def y(self):
        return self._y
    
    def set_x(self, x: int) -> None:
        self._x = x
        
    def set_y(self, y: int) -> None:
        self._y = y

P = Point

class Polygon(object):
    def __init__(self, p: List[Point] = list(), h: List[List[Point]] = list()) -> None:
        self._hull = p
        self._holes = h
        self.l, self.r, self.t, self. b = 0, 0, 0, 0
        
    def set_hull(self, p: List[Point]) -> None:
        if len(p) < 3:
            return
        
        self._hull = p
        self.l = min(pp.x() for pp in p)
        self.r = max(pp.x() for pp in p)
        self.b = min(pp.y() for pp in p)
        self.t = max(pp.y() for pp in p)
            
    def clear(self) -> None:
        self.clear_holes()
        self.clear_hull()
        self.l, self.r, self.t, self. b = 0, 0, 0, 0
        
    def clear_hull(self) -> None:
        self._hull.clear()
        
    def add_hole(self, h: List[Point]) -> None:
        self._holes.append(h)
        
    def clear_holes(self) -> None:
        self._holes.clear()
        
    def __str__(self):
        res = ''
        for h in self._hull:
            res += f'{h.x()},{h.y()} '
            
        if len(self._holes):
            for hole in self._holes:
                res +='\\'
                for h in hole:
                    res += f'{h.x()},{h.y()} '
        
        return res   
    
    def hull(self) -> List[Point]:
        return self._hull
    
    def holes(self) -> List[List[Point]]:
        return self._holes
    
    def bbox(self) -> List[int]:
        '''
        返回 [left, bottom, right, top]
        '''
        return [self.l, self.b, self.r, self.t]
        
        
class PolygonSet(object):
    def __init__(self, pls: List[Polygon] = list()) -> None:
        self._v = pls
        self.l, self.r, self.t, self. b = 0, 0, 0, 0
    
    def load_file(self, file: str) -> Tuple[bool, str]:
        '''
            从文件中导入polygon集合数据
        '''
        self.clear()
        
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    
                    while True:
                        new = line.replace(', ', ',')
                        if new == line:
                            break
                        line = new

                    ls = line.split('\\') # 切分hull 和 hole
                    hull_str = ls[0].replace('\n', '').split(' ')
                    pol = Polygon([],[])
                    hull = list()
                    
                    for h in hull_str:
                        if len(h) == 0:
                            continue
                        xy_str = h.split(',')
                        x = int(xy_str[0])
                        y = int(xy_str[1])
                        hull.append(P(x, y))
                    pol.set_hull(hull)
                    
                    for hole in ls[1:]:
                        ho = list()
                        hole_str = hole.replace('\n', '').split(' ')
                        for h in hole_str:
                            if len(h) == 0:
                                continue
                            xy_str = h.split(',')
                            x = int(xy_str[0])
                            y = int(xy_str[1])
                            ho.append(P(x, y))
                        pol.add_hole(ho.copy())
                        
                    self._v.append(pol)    
                    
                self.l = min(v.bbox()[0] for v in self._v)
                self.r = max(v.bbox()[2] for v in self._v)
                self.b = min(v.bbox()[1] for v in self._v)
                self.t = max(v.bbox()[3] for v in self._v)
                
        except Exception as e:
            # traceback.print_exc()
            err = traceback.format_exc()
            print(err)
            # print(e)
            self.clear
            return False, str(err)
        
        return True, ''
    
    def clear(self) -> None:
        self._v.clear()
        
    def bbox(self) -> List[int]:
        '''
        返回 [left, bottom, right, top]
        '''
        return [self.l, self.b, self.r, self.t]
    
    def __str__(self) -> str:
        res = ''
        for v in self._v:
            res += str(v) + '\n'
        return res
    
    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self._v):
            self.idx += 1
            return self._v[self.idx-1]
        else:
            raise StopIteration
            
    
if __name__ == '__main__':
    # P = Point
    # points = [P(0,0), P(0,10), P(10,10), P(10, 0)]
    # holes = [[P(1,1), P(1,3), P(3,3), P(3, 1)]]
    # polygon = Polygon(points, holes)
    # polygon.add_hole([P(5,5), P(5,8), P(8,8), P(8, 3)])
    # print(polygon)
    
    # pol2 = Polygon()
    # pol2.set_hull([P(0,0), P(100,100), P(0,200)])
    # print(pol2)
    
    
    pls = PolygonSet()
    pls.load_file('polygon.txt')
    # print(pls)
    
    for p in pls:
        print(p)
        print(p.bbox())
    print(pls.bbox())
    
    