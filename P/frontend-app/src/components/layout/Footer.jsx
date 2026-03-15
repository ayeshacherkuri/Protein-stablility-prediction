import React from 'react';
import { Github, Twitter, Linkedin, Heart } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="border-t border-border/40 bg-background py-6 md:py-0">
            <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
                <div className="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
                    <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
                        Built by <span className="font-medium underline underline-offset-4">Advanced Agentic Coding</span>.
                        The source code is available on <span className="font-medium underline underline-offset-4">GitHub</span>.
                    </p>
                </div>
                <div className="flex items-center gap-4">
                    <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                        <Github className="h-5 w-5" />
                    </a>
                    <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                        <Twitter className="h-5 w-5" />
                    </a>
                    <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                        <Linkedin className="h-5 w-5" />
                    </a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
