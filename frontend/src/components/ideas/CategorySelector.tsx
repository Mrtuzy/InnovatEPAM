/**
 * Category selector component
 */
import React, { useEffect, useState } from 'react';
import { getCategories, Category } from '../../api/categories';
import './CategorySelector.css';

interface CategorySelectorProps {
  value: string;
  onChange: (categoryId: string) => void;
  disabled?: boolean;
  error?: string;
}

const CategorySelector: React.FC<CategorySelectorProps> = ({
  value,
  onChange,
  disabled = false,
  error
}) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string>('');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        const data = await getCategories();
        setCategories(data);
        setFetchError('');
      } catch (err) {
        setFetchError('Failed to load categories');
        console.error('Error fetching categories:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  if (loading) {
    return (
      <div className="category-selector">
        <label htmlFor="category-select" className="category-selector-label">
          Category <span className="required">*</span>
        </label>
        <div className="category-selector-loading">Loading categories...</div>
      </div>
    );
  }

  if (fetchError) {
    return (
      <div className="category-selector">
        <label htmlFor="category-select" className="category-selector-label">
          Category <span className="required">*</span>
        </label>
        <div className="category-selector-error">{fetchError}</div>
      </div>
    );
  }

  return (
    <div className="category-selector">
      <label htmlFor="category-select" className="category-selector-label">
        Category <span className="required">*</span>
      </label>
      <select
        id="category-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className={`category-selector-select ${error ? 'error' : ''}`}
        required
      >
        <option value="">Select a category</option>
        {categories.map((category) => (
          <option key={category.id} value={category.id}>
            {category.name}
          </option>
        ))}
      </select>
      {error && <p className="category-selector-error">{error}</p>}
      {value && categories.find(c => c.id === value)?.description && (
        <p className="category-selector-description">
          {categories.find(c => c.id === value)?.description}
        </p>
      )}
    </div>
  );
};

export default CategorySelector;
