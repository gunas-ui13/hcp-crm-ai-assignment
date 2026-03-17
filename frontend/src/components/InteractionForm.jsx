import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateField } from '../store/interactionSlice';

const InteractionForm = () => {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.interaction);

  // This handles whenever a user types in a field
  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateField({ field: name, value }));
  };

  return (
    <div>
      <h2 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '24px' }}>
        Interaction Details
      </h2>

      <form>
        {/* Row 1: HCP Name & Interaction Type */}
        <div className="form-row">
          <div className="form-col">
            <label>HCP Name</label>
            <input 
              type="text" 
              name="hcpName" 
              placeholder="Search or select HCP..." 
              value={formData.hcpName}
              onChange={handleChange}
            />
          </div>
          <div className="form-col">
            <label>Interaction Type</label>
            <select name="interactionType" value={formData.interactionType} onChange={handleChange}>
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Email">Email</option>
            </select>
          </div>
        </div>

        {/* Row 2: Date & Time */}
        <div className="form-row">
          <div className="form-col">
            <label>Date</label>
            <input 
              type="date" 
              name="date" 
              value={formData.date}
              onChange={handleChange}
            />
          </div>
          <div className="form-col">
            <label>Time</label>
            <input 
              type="time" 
              name="time" 
              value="10:00" // Hardcoded for simplicity right now
              onChange={handleChange}
            />
          </div>
        </div>

        {/* Row 3: Topics Discussed */}
        <div className="form-row">
          <div className="form-col">
            <label>Topics Discussed</label>
            <textarea 
              name="notes" 
              placeholder="Enter key discussion points..." 
              rows="4"
              value={formData.notes}
              onChange={handleChange}
            ></textarea>
          </div>
        </div>

        {/* Row 4: Sentiment Radio Buttons */}
        <div style={{ marginBottom: '16px' }}>
          <label>Observed/Inferred HCP Sentiment</label>
          <div style={{ display: 'flex', gap: '16px', marginTop: '8px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 'normal' }}>
              <input 
                type="radio" 
                name="sentiment" 
                value="Positive" 
                checked={formData.sentiment === 'Positive'}
                onChange={handleChange}
              /> Positive
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 'normal' }}>
              <input 
                type="radio" 
                name="sentiment" 
                value="Neutral" 
                checked={formData.sentiment === 'Neutral'}
                onChange={handleChange}
              /> Neutral
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 'normal' }}>
              <input 
                type="radio" 
                name="sentiment" 
                value="Negative" 
                checked={formData.sentiment === 'Negative'}
                onChange={handleChange}
              /> Negative
            </label>
          </div>
        </div>
      </form>
    </div>
  );
};

export default InteractionForm;