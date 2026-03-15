import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Activity, Zap, ShieldCheck, Dna } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/Card';

const Home = () => {
    return (
        <div className="flex flex-col min-h-screen">
            {/* Hero Section */}
            <section className="relative py-20 md:py-32 overflow-hidden bg-background">
                <div className="container relative z-10 flex flex-col items-center text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80 mb-6">
                            <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse"></span>
                            v1.0 Now Available
                        </div>
                        <h1 className="text-4xl font-extrabold tracking-tight lg:text-6xl mb-6">
                            Predict Protein Stability using <br className="hidden md:block" />
                            <span className="text-primary">Advanced Deep Learning</span>
                        </h1>
                        <p className="mx-auto max-w-[700px] text-lg text-muted-foreground mb-8">
                            Analyze amino acid sequences instantly with our CNN-based model.
                            Get accurate stability scores, confidence metrics, and structural insights in seconds.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Link to="/predict">
                                <Button size="lg" className="gap-2">
                                    Start Analysis <ArrowRight className="h-4 w-4" />
                                </Button>
                            </Link>
                            <Link to="/about">
                                <Button variant="outline" size="lg">
                                    Learn More
                                </Button>
                            </Link>
                        </div>
                    </motion.div>

                    {/* Abstract visualization background */}
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/5 rounded-full blur-3xl -z-10" />
                </div>
            </section>

            {/* Features Preview */}
            <section className="py-20 bg-secondary/30">
                <div className="container">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl font-bold tracking-tight mb-4">Why Choose Our Platform?</h2>
                        <p className="text-muted-foreground max-w-2xl mx-auto">
                            Built with cutting-edge technology to provide researchers and students with reliable protein analysis tools.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 }}
                            viewport={{ once: true }}
                        >
                            <Card className="h-full border-none shadow-md">
                                <CardHeader>
                                    <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                                        <Zap className="h-6 w-6 text-primary" />
                                    </div>
                                    <CardTitle>Instant Analysis</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <CardDescription className="text-base">
                                        Get results in milliseconds. Our optimized backend processes sequences rapidly, providing real-time feedback for your research.
                                    </CardDescription>
                                </CardContent>
                            </Card>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                            viewport={{ once: true }}
                        >
                            <Card className="h-full border-none shadow-md">
                                <CardHeader>
                                    <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                                        <Activity className="h-6 w-6 text-primary" />
                                    </div>
                                    <CardTitle>High Accuracy</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <CardDescription className="text-base">
                                        Powered by a Convolutional Neural Network (CNN) trained on thousands of protein sequences to ensure reliable stability predictions.
                                    </CardDescription>
                                </CardContent>
                            </Card>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                            viewport={{ once: true }}
                        >
                            <Card className="h-full border-none shadow-md">
                                <CardHeader>
                                    <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                                        <Dna className="h-6 w-6 text-primary" />
                                    </div>
                                    <CardTitle>Feature Extraction</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <CardDescription className="text-base">
                                        Beyond simple scores, we analyze hydrophobic, charged, and polar amino acid distributions to give you deeper molecular insights.
                                    </CardDescription>
                                </CardContent>
                            </Card>
                        </motion.div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;
