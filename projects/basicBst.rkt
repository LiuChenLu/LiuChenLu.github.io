;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname |basic bst|) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ())))
;
; ********************************************************************
;
; implementing a number of functions for processing binary search
; trees
;
; ********************************************************************
;

; A BST is one of:
; * empty
; * (list key left right) where key is a Num, left and right are
;   BSTs, every key in left is less than key, and every key in right
;   is greater than key.

; sample BSTs
(define forever-alone empty)
(define rage-guy (list 1 empty empty))

(define y-you-no
  (list 5
        (list 3 
              (list  1 empty
                     (list 2 empty empty))
              (list 4 empty empty))
        (list  6 empty empty)))

(define not-bad
  (list 8
        (list 6
              (list 4 empty
                    (list 5 empty empty))
              (list 7 empty empty))
        (list  9 empty empty)))

(define troll
  (list 6 (list 5 empty empty)
        empty))

(define challange-accepted
  (list 6 empty
        (list 7 empty empty)))


; Helper functions

; key:  BST --> Num
; Purpose: produce the key of a non-empty BST.
(define (key t)  (first t))

; left:  BST --> BST
; Purpose:  produce the left subtree of a non-empty BST.
(define (left t) (second t))

; right:  BST --> BST
; Purpose:  produce the right subtree of a non-empty BST.
(define (right t) (third t))

; ********************************************************************
; bst-add: Nat BST -> BST
; purpose consumes a key and a BST to produce a new BST with all the
; keys of the provided BST plus the provided key
; examples
(check-expect (bst-add 1 forever-alone) rage-guy)
(check-expect (bst-add 1 rage-guy) rage-guy)
(check-expect (bst-add 3 y-you-no) y-you-no)
(check-expect (bst-add 3 not-bad) 
              (list 8
                    (list 6
                          (list 4 
                                (list 3 empty empty)
                                (list 5 empty empty))
                          (list 7 empty empty))
                    (list  9 empty empty)))

(define (bst-add provided-key old-bst)
  (cond
    [(empty? old-bst) (list provided-key empty empty)]
    [(< provided-key (first old-bst))
     (list (key old-bst)
           (bst-add provided-key (left old-bst))
           (right old-bst))]
    [(> provided-key (first old-bst))
     (list (key old-bst)
           (left old-bst)
           (bst-add provided-key (right old-bst)))]
    [else old-bst]))

; ********************************************************************
; bst-build: (listof Num) -> BST
; purpose: consumes a list of keys to make a BST that result from
; adding each element to an empty tree
; examples
(check-expect (bst-build empty) forever-alone)
(check-expect (bst-build (list 1)) rage-guy)
(check-expect (bst-build (list 5 3 6 1 4 2)) y-you-no)

(define (bst-build list)
  (local
    [; bst-build-with-acc: (listof Num) (listof Num) -> BST
     ; purpose: help build the BST specified in bst-build by running
     ; an accumulator that keep track of partial solutions
     ; tested through bst-build
     (define (bst-build-with-acc list acc)
       (cond [(empty? list) acc]
             [else (bst-build-with-acc (rest list)
                                       (bst-add (first list) acc))]))]
    (bst-build-with-acc list empty)))

; ********************************************************************
; rot-r: BST -> BST
; purpose: rotates a BST with non-empty left subtree clock-wise so
; that the tree to the right so the root of the left subtree becomes
; the root of the entire tree and the root of the original tree moves 
; into the new right subtree
; examples
(check-expect (rot-r y-you-no)
              (list 3 (list 1 empty (list 2 empty empty))
                    (list 5 (list 4 empty empty)
                          (list 6 empty empty))))
(check-expect (rot-r troll)
              (list 5 empty
                    (list 6 empty empty)))

(define (rot-r bst)
  (list (first (left bst))
        (left (left bst))
        (list (key bst)
              (right (left bst))
              (right bst))))

; ********************************************************************
; rm-root: BST -> BST
; purpose: consumes a BST and produces a BST containing all of the
; same keys except the one at the root
; examples
(check-expect (rm-root forever-alone)
              "error: expected a non-empty bst")
(check-expect (rm-root rage-guy) empty)
(check-expect (rm-root y-you-no)
              (list 3 (list 1 empty (list 2 empty empty))
                    (list 4 empty
                          (list 6 empty empty))))
(check-expect (rm-root troll) (list 5 empty empty))
(check-expect (rm-root challange-accepted) (list 7 empty empty))

(define (rm-root bst)
  (cond [(empty? bst) "error: expected a non-empty bst"]
        [(empty? (left bst)) (right bst)]
        [else (local [; purpose: to provid a rotated bst and to clarify
                      ; the original function
                      (define rotated-bst (rot-r bst))]
                (list (key rotated-bst)
                      (left rotated-bst)
                      (rm-root (right rotated-bst))))]))

; ********************************************************************
; bst-remove: Nat BST -> BST
; purpose: consumes a key and a BST, and produces the BST with the
; node containing the given key removed
; examples
(check-expect (bst-remove 9 forever-alone) forever-alone)
(check-expect (bst-remove 3000 y-you-no) y-you-no)
(check-expect (bst-remove 2 y-you-no)
              (list 5
                    (list 3 
                          (list 1 empty empty)
                          (list 4 empty empty))
                    (list  6 empty empty)))
(check-expect (bst-remove 6 troll) (list 5 empty empty))
(check-expect
 (bst-remove 3 y-you-no)
 (list
  5
  (list 1 empty (list 2 empty (list 4 empty empty)))
  (list 6 empty empty)))

(define (bst-remove unwanted-key bst)
  (cond [(empty? bst) empty]
        [(= unwanted-key (key bst)) (rm-root bst)]
        [(< unwanted-key (key bst))
         (list (key bst) (bst-remove unwanted-key (left bst))
               (right bst))]
        [else ; when (> unwanted-key key)
         (list (key bst) (left bst)
               (bst-remove unwanted-key (right bst)))]))