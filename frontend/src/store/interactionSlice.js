import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  hcpName: '',
  interactionType: 'Meeting',
  date: new Date().toISOString().split('T')[0],
  notes: '',
  sentiment: 'Neutral',
  aiResponse: '',
  isLoading: false,
};

export const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    updateField: (state, action) => {
      const { field, value } = action.payload;
      state[field] = value;
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    setAiResponse: (state, action) => {
      state.aiResponse = action.payload;
    },
    resetForm: () => initialState,
  },
});

export const { updateField, setLoading, setAiResponse, resetForm } = interactionSlice.actions;
export default interactionSlice.reducer;