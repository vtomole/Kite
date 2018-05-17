#!/usr/bin/sbcl --script
;;;Load quicklisp

#-quicklisp
(let ((quicklisp-init (merge-pathnames "/root/quicklisp/setup.lisp"
                                       (user-homedir-pathname))))
  (when (probe-file quicklisp-init)
    (load quicklisp-init)))


(setf ql:*local-project-directories* '(#P"/var/www/"))

(ql:quickload :eagle)

(defun execute (x)
  "Compiles expressions into specified files"
  (print x)
    (case (length x)
       (1 (error "Specify file to compile"))
       (2  (compiler (second x) "/var/www/qc-hack-isu/compiler/a.ir"))
       (3  (compiler (second x) (third x)))
       (t (error "More than 3 arguments"))))

(execute *posix-argv*)
