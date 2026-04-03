export interface ComparisonResult {
  totalDifferences: number;
  addedCount: number;
  removedCount: number;
  modifiedCount: number;
  similarityScore: number;
  originalContentBlocks: ContentBlock[];
  revisedContentBlocks: ContentBlock[];
  addedItems: string[];
  removedItems: string[];
  modifiedItems: ModifiedItem[];
}

export interface ContentBlock {
  id: string;
  type: 'added' | 'removed' | 'modified' | 'unchanged';
  content: string;
  lineNumber?: number;
}

export interface ModifiedItem {
  original: string;
  revised: string;
  lineNumber?: number;
}

export interface FileInfo {
  file: File;
  name: string;
  size: number;
  sizeFormatted: string;
}