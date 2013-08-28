; ********************************************************************
;
; functions working with lists and passing smaller functions as
; parameters
; file includes mapfn, remove-duplicates, cross
;
; ********************************************************************

(provide mapfn remove-duplicates cross)

; ********************************************************************
;
; mapfn function
; demonstraits passing functions as paremeters and use of local
; functions

; A Input is (list Num Num)
; A Function is (Num Num -> (union Num (Listof Num) Boolean)

; mapfn: (listof Function) Input
; -> (listof (union Num (Listof Num) Boolean))
; purpose: takes a list of functions and two numbers and returns a
; list of values returned by operating the function on the two numbers
; examples
;(check-expect (mapfn empty (list 6 9)) empty)
;(check-expect (mapfn (list + *) (list 4 5)) (list 9 20))
;(check-expect (mapfn (list list) (list 2 3)) (list (list 2 3)))
;(check-expect (mapfn (list / -) (list 2 1)) (list 2 1))
;(check-expect (mapfn (list < > = +) (list 1 2))
;              (list true false false 3))

(define (mapfn functions arguments)
  (cond
    [(empty? functions) empty]
    [else (cons (local
                  [; impliment: Function Num Num
                   ; -> (union Num (Listof Num) Boolean)
                   ; purpose: to apply the function listed in
                   ; (listof Functions) to the Input
                   ; tested in mapfn
                   (define (impliment f x y) (f x y))]
             (impliment (first functions)
                        (first arguments) (second arguments)))
           (mapfn (rest functions) arguments))]))

; ********************************************************************
;
; remove-duplicates function
; demonstraits use of unnamed function lambda and racket's built in
; list function filter

; remove-duplicates: (listof Num) -> (listof Num)
; purpose: consumes a list of numbers, and produces the list with all
; but the first occurrence of every number removed
; examples
;(check-expect (remove-duplicates empty) empty)
;(check-expect (remove-duplicates '(1 2 3)) '(1 2 3))
;(check-expect (remove-duplicates '(1 2 1 3)) '(1 2 3))
;(check-expect (remove-duplicates '(1 1 1 1)) '(1))
;(check-expect (remove-duplicates '(1 2 1 2)) '(1 2))
;(check-expect (remove-duplicates '(1 2 1 2 5 6 4 5 6 3 3 9))
;              '(1 2 5 6 4 3 9))

(define (remove-duplicates list)
  (foldr (lambda (x y)
           (cons x (filter (lambda (z)
                             (not (= z x)))
                           y)))
           empty
           list))

; ********************************************************************
;
; cross function
; demonstraits use of unnamed function lambda, racket's built in
; list function map and foldr

; purpose: consumes a list of symbols and a list of numbers and
; produces all possible pairs of symbols and numbers
; example
;(cross empty empty) -> empty
;(cross empty '(1 2))-> empty
;(check-expect (cross '(d r c) '(1 2)) ->
;              (list (list 'd 1) (list 'd 2) (list 'r 1) (list 'r 2)
;                    (list 'c 1) (list 'c 2))

(define (cross list1 list2)
  (foldr append
         empty
         (map (λ (current-list1)
                (map (λ (current-list2)
                       (list current-list1 current-list2))
                     list2))
                list1)))