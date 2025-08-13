# Text Verification Feature - User Guide

## Overview

The Text Verification feature allows you to verify and edit detected mite text directly in the image preview interface. This feature becomes active after analysis completion and includes automatic zone locking to prevent accidental modifications.

## How to Use

### Step 1: Run Analysis
1. Launch the Modern Varroa Detector GUI
2. Select your dataset folder
3. Configure analysis settings (plates per recording, etc.)
4. Click "🚀 Start Analysis" and wait for completion

### Step 2: Automatic Zone Locking
After analysis completes:
- ✅ Zones automatically lock (red borders with 🔒 icons)
- ✅ Zone selection controls become disabled
- ✅ Zone status shows "🔒 Zones Locked" 
- ✅ Click indicators appear on zones

### Step 3: Interactive Zone Exploration
- **Hover over zones**: See mite information in the right panel
- **Zone details**: View zone class, coordinates, and mite count
- **Real-time updates**: Information updates as you move your mouse
- **Visual feedback**: Cursor changes to hand when over clickable zones

### Step 4: Text Verification
1. **Click on a zone** containing mites
2. **Verification dialog opens** showing all mites in that zone
3. **Edit text** for each mite individually
4. **Save changes** or cancel if needed
5. **Status updates**: Verified mites show ✅ in the mite list

## Interface Elements

### Zone Information Panel (Right Side)
- **Zone Status**: Shows if zones are locked/unlocked
- **Current Zone**: Information about hovered zone
- **Detected Mites**: List of all mites with verification status
- **Verification Controls**: Button to enable text verification mode

### Visual Indicators
- 🔓 **Unlocked zones**: Blue/green borders, editable
- 🔒 **Locked zones**: Red borders with lock icons
- ✅ **Verified mites**: Green checkmark in mite list
- ⏳ **Unverified mites**: Clock icon in mite list
- 🖱️ **Clickable zones**: Hand cursor when hovering

### Text Verification Dialog
- **Zone title**: Shows which zone you're editing
- **Mite information**: Status (alive/dead) and detection metrics
- **Text fields**: Individual text entry for each mite
- **Save/Cancel**: Buttons to confirm or discard changes

## Workflow Example

```
1. Select dataset folder → Zones visible with blue/green borders
2. Run analysis → Progress bar shows analysis status
3. Analysis completes → Zones lock automatically (red borders)
4. Hover over Zone 1 → "Zone 1: 3 mites detected" appears
5. Click Zone 1 → Dialog opens with 3 mites to verify
6. Edit text for each mite → Save changes
7. Mite list updates → Verified mites show ✅
8. Repeat for other zones as needed
```

## Features

### ✅ What Works
- Automatic zone locking after analysis
- Interactive hover information
- Click-to-edit text verification
- Real-time status updates
- Visual feedback for all actions
- Individual mite text editing
- Verification status tracking

### 🔧 Requirements
- Dataset folder with images
- Completed analysis run
- Zone coordinates file (automatically generated)
- Analysis results (CSV format)

## Troubleshooting

### No zones visible?
- Ensure you've selected a dataset folder
- Check that zone coordinates files exist in `Zoning/` folder
- Verify plates per recording setting matches your data

### Can't click on zones?
- Make sure analysis has completed successfully
- Verify zones are locked (red borders with 🔒)
- Check that mites were detected in the zone

### No mite information?
- Confirm analysis produced results (CSV files)
- Check `outputs/` folder for analysis results
- Try the demo script to test functionality

### Dialog not opening?
- Ensure the zone contains detected mites
- Check console for error messages
- Verify text verification is enabled

## Testing

Run the test suite to verify functionality:
```bash
python test_text_verification_integration.py
```

Run the demo to see features in action:
```bash
python demo_text_verification.py
```

## Technical Details

- **Interactive canvas**: Replaces static image display
- **Event handling**: Mouse hover, click, and leave events
- **Coordinate transformation**: Accurate zone detection
- **Data management**: CSV parsing with fallback options
- **UI updates**: Real-time information panel updates

## Tips

1. **Efficient workflow**: Complete all text verification before final export
2. **Visual cues**: Use the status indicators to track progress
3. **Batch processing**: Verify multiple zones systematically
4. **Save frequently**: Changes are saved immediately when you click Save
5. **Error recovery**: Cancel dialog if you make mistakes

## Next Steps

After verifying text:
1. Download your results as usual
2. Exported files will include verified text data
3. Use the ZIP download feature for complete results
4. Review analysis reports with verified information

---

For technical details and integration information, see `TEXT_VERIFICATION_INTEGRATION.md`.
