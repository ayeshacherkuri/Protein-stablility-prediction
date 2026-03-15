import React from 'react';
import { Mail, MessageSquare, MapPin } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/Card';

const Contact = () => {
    const handleSubmit = (e) => {
        e.preventDefault();
        alert("Thank you for your message! This is a demo form.");
    };

    return (
        <div className="container py-12 md:py-20 max-w-5xl">
            <div className="grid md:grid-cols-2 gap-12">

                {/* Contact Info */}
                <div>
                    <h1 className="text-4xl font-bold mb-6">Get in Touch</h1>
                    <p className="text-muted-foreground text-lg mb-8">
                        Have questions about the model, suggestions for improvement, or just want to say hi?
                        We'd love to hear from you.
                    </p>

                    <div className="space-y-6">
                        <div className="flex items-start gap-4">
                            <div className="bg-primary/10 p-3 rounded-lg">
                                <Mail className="h-6 w-6 text-primary" />
                            </div>
                            <div>
                                <h3 className="font-semibold">Email Us</h3>
                                <p className="text-muted-foreground">support@proteinstability.ai</p>
                            </div>
                        </div>

                        <div className="flex items-start gap-4">
                            <div className="bg-primary/10 p-3 rounded-lg">
                                <MessageSquare className="h-6 w-6 text-primary" />
                            </div>
                            <div>
                                <h3 className="font-semibold">Community</h3>
                                <p className="text-muted-foreground">Join our Discord server</p>
                            </div>
                        </div>

                        <div className="flex items-start gap-4">
                            <div className="bg-primary/10 p-3 rounded-lg">
                                <MapPin className="h-6 w-6 text-primary" />
                            </div>
                            <div>
                                <h3 className="font-semibold">Location</h3>
                                <p className="text-muted-foreground">Research Lab, Dept of CS</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Contact Form */}
                <Card>
                    <CardHeader>
                        <CardTitle>Send a Message</CardTitle>
                        <CardDescription>We'll get back to you as soon as possible.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label htmlFor="first-name" className="text-sm font-medium">First name</label>
                                    <input id="first-name" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" required />
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="last-name" className="text-sm font-medium">Last name</label>
                                    <input id="last-name" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" required />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label htmlFor="email" className="text-sm font-medium">Email</label>
                                <input id="email" type="email" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" required />
                            </div>

                            <div className="space-y-2">
                                <label htmlFor="message" className="text-sm font-medium">Message</label>
                                <textarea id="message" className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" required></textarea>
                            </div>

                            <Button type="submit" className="w-full">
                                Send Message
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default Contact;
