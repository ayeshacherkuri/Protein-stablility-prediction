import React from 'react';
import { Card, CardContent } from '../components/ui/Card';

const About = () => {
    return (
        <div className="container py-12 md:py-20 max-w-4xl">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold mb-4">About the Project</h1>
                <p className="text-muted-foreground text-lg">
                    Bridging the gap between deep learning and bioinformatics.
                </p>
            </div>

            <div className="space-y-12">
                {/* Mission Section */}
                <section>
                    <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
                    <p className="leading-relaxed text-muted-foreground">
                        Protein stability is a fundamental property that determines a protein's function and reliability in biological systems.
                        Traditional methods for determining stability are often time-consuming and expensive wet-lab experiments.
                        Our mission is to provide a reliable, fast, and accessible computational tool that leverages the power of Convolutional Neural Networks (CNNs)
                        to predict protein stability directly from amino acid sequences.
                    </p>
                </section>

                {/* Technology Section */}
                <section>
                    <h2 className="text-2xl font-semibold mb-4">Under the Hood</h2>
                    <div className="grid md:grid-cols-2 gap-6">
                        <Card>
                            <CardContent className="pt-6">
                                <h3 className="font-semibold mb-2">Deep Learning Model</h3>
                                <p className="text-sm text-muted-foreground">
                                    We utilize a 1D Convolutional Neural Network (CNN) architecture optimized for sequence analysis.
                                    The model extracts local patterns and motifs from the amino acid sequence to infer structural stability.
                                </p>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardContent className="pt-6">
                                <h3 className="font-semibold mb-2">Dataset</h3>
                                <p className="text-sm text-muted-foreground">
                                    The model was trained on a comprehensive dataset of experimentally verified protein stability measurements,
                                    ensuring that predictions are grounded in real-world biological data.
                                </p>
                            </CardContent>
                        </Card>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default About;
