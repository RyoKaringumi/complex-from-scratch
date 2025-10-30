from __future__ import annotations

"""
(x+y)/z = x/z + y/z である
これを証明するために、まず両方にzを掛ける
(x+y) = (x/z)*z + (y/z)*z となる
ここで、(x/z)*z = x であり、(y/z)*z = y であるため、
(x+y) = x + y となり、等式が成り立つ
"""

class Complex:
    """
    内部的には real+imag*i という式である
    
    実際メモリ上には、実部と虚部の二つのfloat型の数値が保存されている
    各演算は、複素数の定義に基づいて実装されている
    
    基本的に、二項演算子の場合、
    a = self.real
    b = self.imag
    c = other.real
    d = other.imag
    として、計算を行う
    
    iは虚数単位であり、i*i = -1 である
    """
    
    real: float # 実部
    imag: float # 虚部
    
    def __init__(self, real: float, imag: float) -> None:
        self.real = real
        self.imag = imag
        
    @staticmethod
    def valueOf(value: object) -> Complex:
        """
        渡された値をComplex型に変換する
        
        実数であれば、虚部0の複素数に変換する
        Python組み込みのcomplex型であれば、Complex型に変換する
        Complex型であれば、そのまま返す
        それ以外の型であれば、TypeErrorを投げる
        """
        if isinstance(value,(int,float)):
            #実数が渡されたなら、これを複素数にする
            # 虚部が0の場合、それはただの実数と同じのため、今後の演算処理のために複素数に変換する
            return Complex(float(value),0)
        if isinstance(value,complex):
            # Python組み込みのcomplex型が渡されたなら、これをComplexに変換する
            return Complex(value.real,value.imag)
        if isinstance(value,Complex):
            # Complex型が渡されたなら、そのまま返す
            return value
        raise TypeError(f"Cannot convert {type(value)} to Complex")
        

    def __add__(self,other:object)->Complex:
        """
        二つの複素数を足し合わせる場合、式は
        (a + b*i) + (c + d*i) になる
        複素数は多項式であるため、整理出来る
        = a + c + (b + d)*i となる
        よって、実部同士、虚部同士を足し合わせれば良い
        """
        other = Complex.valueOf(other)
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag

        real = a + c
        imag = b + d
        return Complex(real,imag)

    def __sub__(self,other:object)->Complex:
        """
        上記の足し算の処理と同様であり、
        (a + b*i) - (c + d*i)
        = (a - c) + (b - d)*i となる
        よって、実部同士、虚部同士を引き算すれば良い
        """
        other = Complex.valueOf(other)
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag

        real = a - c
        imag = b - d
        return Complex(real,imag)

    def __mul__(self,other:object)->Complex:
        """
        複素数の掛け算は、
        (a + b*i) * (c + d*i) になる
        先ほどは単純に繋げる事が出来たが、掛け算のため、分配法則を使う必要がある
        分配法則とは、(x+y)(u+v) = xu + xv + yu + yv である
        よって、上記の式は
        = a*c + a*d*i + b*i*c + b*i*d*i となる
        ここで、iは虚数であり、i*i = -1 であるため、
        = a*c + a*d*i + b*c*i - b*d となる
        これを整理していく
        iが掛かっていない項同士、iが掛かっている項同士でまとめると
        = (a*c - b*d) + (a*d + b*c)*i となる
        よって、実部と虚部をそれぞれ計算すれば良い
        
        つまり、
        実数部は a*c - b*d であり
        虚数部は a*d + b*c である
        """
        other = Complex.valueOf(other)
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag

        real = a*c - b*d
        imag = a*d + b*c
        return Complex(real,imag)
    
    def conjugate(self)->Complex:
        """
        共役複素数を返す
        共役複素数とは、虚部の符号を反転させたものである
        つまり、a + b*i の共役複素数は a - b*i である
        """
        return Complex(self.real,-self.imag)
    
    def __truediv__(self,other:object)->Complex:
        """
        複素数の割り算は
        (a + b*i) / (c + d*i) になる
        複素数の割り算は、分母の虚数成分を消すために、分子と分母に分母の共役複素数を掛ける
        分数は分母と分子両方に同じ数を掛けても値が変わらないため、これを利用する
        
        共役複素数とは、虚部の符号を反転させたものである
        つまり、a + b*i の共役複素数は a - b*i である
        
        これを両方に掛け合わせると
        (a + b*i) * (c - d*i) / (c + d*i) * (c - d*i) になる
        
        まず、分母に注目し、計算を行う
        分母: (c + d*i) * (c - d*i)
        これは、複素数同士の掛け算であるため、上記の掛け算の処理を使う
        しかし、引き算が問題であるため、
        = (c + d*i) * (c + (d*-1)*i)
        掛け算のやり方は (a*c - b*d) + (a*d + b*c)*iであったため、今回の分母に当てはめると
        (c*c - d*(d*-1)) + (c*(d*-1) + d*c)*iになる
        まず、軽く整理すると
        = (c*c + d*d) + (c*(d*-1) + d*c)*i
        = (c*c + d*d) + ( -c*d + d*c)*i
        虚数部分で-cと+cが打ち消し合うため0になり、
        = (c*c + d*d) + 0*i となり、虚数成分が消える
        
        次に、分子に注目し、計算を行う
        分子: (a + b*i) * (c - d*i)
        これは、複素数同士の掛け算であるため、上記の掛け算の処理を使う
        しかし、引き算が問題であるため、
        = (a + b*i) * (c + (d*-1)*i)
        掛け算のやり方は (a*c - b*d) + (a*d + b*c)*iであったため、今回の分子に当てはめると
        = (a*c - b*(d*-1)) + (a*(d*-1) + b*c)*i
        = (a*c + b*d) + (-a*d + b*c)*i これは(d*-1を - d に変換した)
        = (a*c + b*d) + (b*c - a*d)*i 順序を並び替え
        となる
        
        まとめると、
        分母分子をまとめると、
        ((a*c + b*d) + (b*c - a*d)*i) / (c*c + d*d) となる
        
        しかし、このままだと分子側にIが残っているため、実部と虚部に分ける必要がある
        そのため、分数の分配法則を使う
        分数の分配法則とは、(x + y)/z = x/z + y/z である    
        
        これを使うと、
        = ((a*c + b*d) / (c*c + d*d)) + ((b*c - a*d) / (c*c + d*d))*i となる
        これで、実部と虚部が分離されたため、各々を計算すれば良い
        つまり、
        実部は (a*c + b*d) / (c*c + d*d)
        虚部は (b*c - a*d) / (c*c + d*d) である
        """
        other = Complex.valueOf(other)
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag

        denominator = c*c + d*d
        real = (a*c + b*d) / denominator
        imag = (b*c - a*d) / denominator
        return Complex(real,imag)
