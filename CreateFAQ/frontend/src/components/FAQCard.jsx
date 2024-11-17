/*
 * -----------------------------------------------------------------------
 * File: frontend/FAQCard.js
 * Creation Time: Nov 16th 2024, 8:06 pm
 * Author: Saurabh Zinjad
 * Developer Email: saurabhzinjad@gmail.com
 * Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
 * -----------------------------------------------------------------------
 */

import React from 'react';

const FAQCard = ({ question, answer, tags }) => {
	return (
		<div className='card bg-base-100 shadow-md my-4'>
			<div className='card-body'>
				<h2 className='card-title text-lg font-semibold'>{question}</h2>
				<p className='mt-2'>{answer}</p>
				<div className='mt-4 flex flex-wrap gap-2'>
					{tags.map((tag, index) => (
						<span key={index} className='badge badge-outline'>
							{tag}
						</span>
					))}
				</div>
			</div>
		</div>
	);
};

export default FAQCard;
