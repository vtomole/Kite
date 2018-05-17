all: 
	wget "https://beta.quicklisp.org/release-key.txt" 
	wget "https://beta.quicklisp.org/quicklisp.lisp"
	wget "https://beta.quicklisp.org/quicklisp.lisp.asc"
	gpg --import release-key.txt 
	gpg --verify quicklisp.lisp.asc quicklisp.lisp 
	sync 
	sleep 2 
	rm -rf "$GNUPGHOME" quicklisp.lisp.asc 
	sbcl --no-sysinit --no-userinit --non-interactive --load quicklisp.lisp --eval "(quicklisp-quickstart:install)" --eval "(ql::without-prompting (dolist (imp '(:sbcl)) (ql:add-to-init-file imp)))"
