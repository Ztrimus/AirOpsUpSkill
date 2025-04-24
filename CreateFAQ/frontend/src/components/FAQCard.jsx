import React, { useState } from 'react';
import { FaThumbsUp, FaThumbsDown } from 'react-icons/fa';

const FAQCard = ({
	faq_name,
	machine_type,
	common_3_repairs,
	common_3_culprits,
	solution_to_single_frequent_culprit,
	rating,
	onFeedback,
}) => {
	const [showFullSolution, setShowFullSolution] = useState(false);

	const toggleSolution = () => {
		setShowFullSolution((prev) => !prev);
	};

	return (
		<div
			className='glass-card p-6 rounded-lg shadow-md hover:shadow-2xl hover:scale-105 transition-transform duration-300 border border-gray-200'
			style={{
				background: 'rgba(255, 255, 255, 0.15)',
				boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
				backdropFilter: 'blur(10px)',
			}}
		>
			<div>
				{/* FAQ Title */}
				<h2 className='text-xl font-bold mb-2'>{faq_name}</h2>
				<p className='text-sm text-gray-500 mb-4 flex gap-2'>
					<span>⚙️</span> {machine_type}
				</p>

				{/* Common Repairs */}
				<div className='mb-4'>
					<h3 className='text-blue-500 font-medium flex gap-2'>
						<span>🔧</span> <b>Common Repairs</b>
					</h3>
					<ul className='list-disc list-inside text-gray-700 mt-1 text-sm'>
						{common_3_repairs.split(', ').map((repair, index) => (
							<li key={index}>{repair}</li>
						))}
					</ul>
				</div>

				{/* Common Culprits */}
				<div className='mb-4'>
					<h3 className='text-orange-500 font-medium flex gap-2'>
						<span>⚠️</span> <b>Common Culprits</b>
					</h3>
					<ul className='list-disc list-inside text-gray-700 mt-1 text-sm'>
						{common_3_culprits.split(', ').map((culprit, index) => (
							<li key={index}>{culprit}</li>
						))}
					</ul>
				</div>

				{/* Solution */}
				<div>
					<h3 className='text-green-500 font-medium flex gap-2'>
						<span>✅</span> <b>Solution</b>
					</h3>
					<p className='text-gray-700 mt-1 text-sm'>
						{showFullSolution
							? solution_to_single_frequent_culprit
							: `${solution_to_single_frequent_culprit.slice(0, 200)}...`}
					</p>
					{solution_to_single_frequent_culprit.length > 200 && (
						<button
							className='text-blue-500 text-sm mt-2 underline'
							onClick={toggleSolution}
						>
							{showFullSolution ? 'Show less' : 'Show more'}
						</button>
					)}
				</div>
			</div>

			{/* Feedback Buttons - Sticky Footer */}
			<div className='mt-6 flex justify-between border-t pt-4 border-gray-500'>
				<span className='text-sm text-gray-600'>Rating: {rating}</span>
				<div className='flex gap-2'>
					<button
						className='flex justify-center text-emerald-500 border border-emerald-500 px-3 py-1 text-sm rounded-md hover:bg-emerald-500 hover:text-white transition-all'
						onClick={() => onFeedback('helpful')}
					>
						<FaThumbsUp className='mr-1' /> {/* Thumbs Up Icon */}
					</button>
					<button
						className='flex justify-center text-rose-500 border border-rose-500 px-3 py-1 text-sm rounded-md hover:bg-rose-500 hover:text-white transition-all'
						onClick={() => onFeedback('improve')}
					>
						<FaThumbsDown className='mr-1' /> {/* Thumbs Down Icon */}
					</button>
				</div>
			</div>
		</div>
	);
};

export default FAQCard;
