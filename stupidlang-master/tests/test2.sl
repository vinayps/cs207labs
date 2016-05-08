(def rad 5)
rad
(def radiusfunc (func (radius) (* pi (* radius radius))))
(radiusfunc rad)
(def myvar 0)
(if (== myvar 1) (store rad 6) (store rad 7))
(radiusfunc rad)
(== 1 1)
(def area (radiusfunc rad))
rad
