import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, Activity, ShieldCheck, Zap } from 'lucide-react';
import { cn } from '../../lib/utils';
import { motion } from 'framer-motion';

const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const location = useLocation();

    const navLinks = [
        { name: 'Home', path: '/' },
        { name: 'Features', path: '/features' },
        { name: 'Predict', path: '/predict' },
        { name: 'About', path: '/about' },
        { name: 'Contact', path: '/contact' },
    ];

    const toggler = () => setIsOpen(!isOpen);

    return (
        <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-16 items-center justify-between">
                <Link to="/" className="flex items-center space-x-2">
                    <div className="bg-primary text-primary-foreground p-1 rounded-md">
                        <Activity className="h-6 w-6" />
                    </div>
                    <span className="font-heading font-bold text-xl hidden sm:inline-block">
                        ProteinStability<span className="text-primary/70">AI</span>
                    </span>
                </Link>

                {/* Desktop Nav */}
                <div className="hidden md:flex items-center space-x-6">
                    {navLinks.map((link) => (
                        <Link
                            key={link.path}
                            to={link.path}
                            className={cn(
                                "text-sm font-medium transition-colors hover:text-primary",
                                location.pathname === link.path
                                    ? "text-primary font-semibold"
                                    : "text-muted-foreground"
                            )}
                        >
                            {link.name}
                        </Link>
                    ))}
                    <Link to="/predict">
                        <button className="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md text-sm font-medium transition-colors">
                            Get Started
                        </button>
                    </Link>
                </div>

                {/* Mobile Menu Button */}
                <button className="md:hidden p-2 text-muted-foreground" onClick={toggler}>
                    {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                </button>
            </div>

            {/* Mobile Nav */}
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="md:hidden border-b border-border bg-background p-4"
                >
                    <div className="flex flex-col space-y-4">
                        {navLinks.map((link) => (
                            <Link
                                key={link.path}
                                to={link.path}
                                onClick={toggler}
                                className={cn(
                                    "text-base font-medium transition-colors hover:text-primary p-2 rounded-md hover:bg-muted",
                                    location.pathname === link.path
                                        ? "text-primary bg-muted font-semibold"
                                        : "text-muted-foreground"
                                )}
                            >
                                {link.name}
                            </Link>
                        ))}
                        <Link to="/predict" onClick={toggler}>
                            <button className="w-full bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md text-sm font-medium transition-colors">
                                Get Started
                            </button>
                        </Link>
                    </div>
                </motion.div>
            )}
        </nav>
    );
};

export default Navbar;
