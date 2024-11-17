/*
 * -----------------------------------------------------------------------
 * File: frontend/FAQList.js
 * Creation Time: Nov 16th 2024, 8:07 pm
 * Author: Saurabh Zinjad
 * Developer Email: saurabhzinjad@gmail.com
 * Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
 * -----------------------------------------------------------------------
 */

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import FAQCard from './FAQCard';

const FAQList = ({ searchQuery }) => {
	const [faqs, setFaqs] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const fetchFAQs = async () => {
			try {
				setLoading(true);
				const response = await axios.get(`http://localhost:8000/faqs?query=${searchQuery}`);
				setFaqs(response.data);
			} catch (error) {
				console.error('Error fetching FAQs:', error);
			} finally {
				setLoading(false);
			}
		};

		fetchFAQs();
	}, [searchQuery]);

	if (loading) return <p>Loading FAQs...</p>;

	return (
		<div>
			{faqs.length > 0 ? (
				faqs.map((faq) => (
					<FAQCard
						key={faq.id}
						question={faq.question}
						answer={faq.answer}
						tags={faq.tags || []}
					/>
				))
			) : (
				<p>No FAQs found for your query.</p>
			)}
		</div>
	);
};

export default FAQList;
