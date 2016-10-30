function dct(mas) {
    for (var i = 0; i<8; i++) {        
        Ci = (i==0) ? (1/sqrt(2)) : 1;
        for (var j = 0; j<8*3; j+=3) {
            Cj = (j==0) ? (1/sqrt(2)) : 1;
            var sum = 0;
            var k = 0;
            for(var x =0; x<8; x++) {
                var m = 1;
                for(var y =0; y<8; y++) {
                    sum = mas[x][y+m] * cos(((2*y+1)*k*Math.PI)/(2*8)) * cos(((2*x+1)*i*Math.PI)/(2*8))
                    m+=2;
                    k++;
                }
            }     
            mas[y][j+1] = (1/sqrt(2*8))*Ci*Cj*sum;
        }
    }
}